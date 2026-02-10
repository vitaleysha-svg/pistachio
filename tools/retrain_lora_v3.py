#!/usr/bin/env python3
"""Train LoRA v3 with regularization images, Prodigy optimizer, and auto-captioning.

Example:
  python3 retrain_lora_v3.py \
    --train-data-dir /workspace/lora_dataset_v3/10_amiranoor \
    --reg-data-dir /workspace/reg_images/1_woman \
    --pretrained-model /workspace/models/sd_xl_base_1.0.safetensors
"""

from __future__ import annotations

import argparse
import hashlib
import shutil
import subprocess
import sys
from pathlib import Path

PINNED_DEPENDENCIES = {
    "transformers": "4.38.2",
    "diffusers": "0.25.1",
    "huggingface_hub": "0.21.4",
    "accelerate": "0.27.2",
    "safetensors": "0.4.2",
    "bitsandbytes": "0.43.1",
    "voluptuous": "0.15.2",
    "imagesize": "1.4.1",
    "toml": "0.10.2",
    "prodigyopt": "1.1.2",
}


def run(cmd: list[str]) -> None:
    print("[cmd]", " ".join(str(x) for x in cmd))
    subprocess.run(cmd, check=True)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def ensure_dependencies(skip_install: bool) -> None:
    missing = []
    for package, version in PINNED_DEPENDENCIES.items():
        import_name = package
        if package == "prodigyopt":
            import_name = "prodigyopt"
        try:
            __import__(import_name)
        except Exception:  # noqa: BLE001
            missing.append(f"{package}=={version}")

    if not missing:
        return
    if skip_install:
        raise RuntimeError(
            "Missing dependencies: " + ", ".join(missing) + ". Re-run without --skip-install."
        )
    run([sys.executable, "-m", "pip", "install", "--no-input", *missing])


def write_dataset_config(path: Path, args: argparse.Namespace) -> None:
    dataset_toml = f"""[general]
shuffle_caption = true
caption_extension = '{args.caption_extension}'
keep_tokens = 1

[[datasets]]
resolution = {args.resolution}
batch_size = {args.train_batch_size}
enable_bucket = true
min_bucket_reso = 512
max_bucket_reso = 1536

  [[datasets.subsets]]
  image_dir = '{args.train_data_dir.as_posix()}'
  num_repeats = {args.train_repeats}

  [[datasets.subsets]]
  image_dir = '{args.reg_data_dir.as_posix()}'
  is_reg = true
  class_tokens = '{args.class_tokens}'
  num_repeats = {args.reg_repeats}
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(dataset_toml, encoding="utf-8")
    print(f"[ok] Wrote dataset config: {path}")


def count_images(path: Path) -> int:
    extensions = {".jpg", ".jpeg", ".png", ".webp", ".bmp"}
    return sum(1 for p in path.rglob("*") if p.is_file() and p.suffix.lower() in extensions)


def run_auto_caption(args: argparse.Namespace) -> None:
    script_path = args.auto_caption_script
    if not script_path.exists():
        raise FileNotFoundError(
            f"Auto-caption script not found: {script_path}. Upload tools/auto_caption.py to pod."
        )

    cmd = [
        sys.executable,
        str(script_path),
        "--input-dir",
        str(args.train_data_dir),
        "--trigger-word",
        args.trigger_word,
    ]
    if args.force_recaption:
        cmd.append("--overwrite")
    run(cmd)


def run_dataset_manifest(args: argparse.Namespace) -> tuple[Path, str]:
    if args.skip_dataset_manifest:
        return args.dataset_manifest_out, ""

    script_path = args.dataset_manifest_script
    if not script_path.exists():
        raise FileNotFoundError(
            f"Dataset manifest script not found: {script_path}. Upload tools/dataset_manifest.py to pod."
        )

    args.dataset_manifest_out.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        sys.executable,
        str(script_path),
        "--dataset-dir",
        str(args.train_data_dir),
        "--caption-extension",
        args.caption_extension,
        "--output",
        str(args.dataset_manifest_out),
    ]
    run(cmd)
    manifest_hash = sha256_file(args.dataset_manifest_out)
    print(f"[manifest] path={args.dataset_manifest_out} sha256={manifest_hash}")
    return args.dataset_manifest_out, manifest_hash


def build_training_command(args: argparse.Namespace) -> list[str]:
    train_script = args.sd_scripts_dir / "sdxl_train_network.py"
    if not train_script.exists():
        raise FileNotFoundError(f"Missing training script: {train_script}")

    cmd: list[str] = [
        sys.executable,
        "-m",
        "accelerate.commands.launch",
        "--num_cpu_threads_per_process",
        "2",
        str(train_script),
        "--pretrained_model_name_or_path",
        str(args.pretrained_model),
        "--dataset_config",
        str(args.dataset_config),
        "--output_dir",
        str(args.output_dir),
        "--output_name",
        args.output_name,
        "--save_model_as",
        "safetensors",
        "--prior_loss_weight",
        str(args.prior_loss_weight),
        "--max_train_steps",
        str(args.max_train_steps),
        "--learning_rate",
        str(args.unet_learning_rate),
        "--optimizer_type",
        "Prodigy",
        "--optimizer_args",
        "decouple=True",
        "weight_decay=0.01",
        "betas=[0.9,0.99]",
        "use_bias_correction=True",
        "safeguard_warmup=True",
        "--lr_scheduler",
        "cosine",
        "--lr_warmup_steps",
        str(args.lr_warmup_steps),
        "--xformers",
        "--mixed_precision",
        "fp16",
        "--save_precision",
        "fp16",
        "--cache_latents",
        "--gradient_checkpointing",
        "--max_data_loader_n_workers",
        "0",
        "--persistent_data_loader_workers",
        "--network_module",
        "networks.lora",
        "--network_dim",
        str(args.network_dim),
        "--network_alpha",
        str(args.network_alpha),
        "--train_batch_size",
        str(args.train_batch_size),
        "--save_every_n_steps",
        str(args.save_every_n_steps),
        "--seed",
        str(args.seed),
        "--caption_extension",
        args.caption_extension,
        "--logging_dir",
        str(args.logging_dir),
        "--log_prefix",
        args.output_name,
    ]

    if args.train_text_encoder:
        cmd.extend(["--text_encoder_lr", str(args.text_encoder_learning_rate)])
    else:
        cmd.append("--network_train_unet_only")

    return cmd


def copy_outputs_to_comfyui(args: argparse.Namespace) -> None:
    if not args.comfyui_lora_dir:
        return
    target_dir = args.comfyui_lora_dir
    target_dir.mkdir(parents=True, exist_ok=True)

    for src in sorted(args.output_dir.glob(f"{args.output_name}*.safetensors")):
        dst = target_dir / src.name
        shutil.copy2(src, dst)
        print(f"[ok] Copied to ComfyUI: {dst}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Train LoRA v3 with regularization and Prodigy.")
    parser.add_argument("--sd-scripts-dir", type=Path, default=Path("/workspace/sd-scripts"))
    parser.add_argument(
        "--pretrained-model",
        type=Path,
        default=Path("/workspace/models/sd_xl_base_1.0.safetensors"),
    )
    parser.add_argument(
        "--train-data-dir",
        type=Path,
        default=Path("/workspace/lora_dataset_v3/10_amiranoor"),
    )
    parser.add_argument("--reg-data-dir", type=Path, default=Path("/workspace/reg_images/1_woman"))
    parser.add_argument("--class-tokens", default="woman")
    parser.add_argument("--output-dir", type=Path, default=Path("/workspace/lora_output_v3"))
    parser.add_argument("--output-name", default="amiranoor_v3")
    parser.add_argument("--trigger-word", default="amiranoor")
    parser.add_argument("--dataset-config", type=Path, default=Path("/workspace/lora_output_v3/dataset_config_v3.toml"))
    parser.add_argument("--logging-dir", type=Path, default=Path("/workspace/lora_output_v3/logs"))

    parser.add_argument("--resolution", type=int, default=1024)
    parser.add_argument("--train-batch-size", type=int, default=1)
    parser.add_argument("--train-repeats", type=int, default=10)
    parser.add_argument("--reg-repeats", type=int, default=1)
    parser.add_argument("--max-train-steps", type=int, default=2500)
    parser.add_argument("--save-every-n-steps", type=int, default=500)
    parser.add_argument("--network-dim", type=int, default=32)
    parser.add_argument("--network-alpha", type=int, default=16)
    parser.add_argument("--unet-learning-rate", type=float, default=1e-4)
    parser.add_argument("--text-encoder-learning-rate", type=float, default=5e-6)
    parser.add_argument("--prior-loss-weight", type=float, default=1.0)
    parser.add_argument("--lr-warmup-steps", type=int, default=100)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--caption-extension", default=".txt")
    parser.add_argument("--train-text-encoder", action="store_true")

    parser.add_argument("--auto-caption-script", type=Path, default=Path("/workspace/auto_caption.py"))
    parser.add_argument("--dataset-manifest-script", type=Path, default=Path(__file__).with_name("dataset_manifest.py"))
    parser.add_argument("--dataset-manifest-out", type=Path, default=None)
    parser.add_argument("--skip-dataset-manifest", action="store_true")
    parser.add_argument("--skip-auto-caption", action="store_true")
    parser.add_argument("--force-recaption", action="store_true")
    parser.add_argument(
        "--comfyui-lora-dir",
        type=Path,
        default=Path("/workspace/runpod-slim/ComfyUI/models/loras"),
    )
    parser.add_argument("--skip-install", action="store_true")
    return parser.parse_args()


def validate_inputs(args: argparse.Namespace) -> None:
    if not args.pretrained_model.exists():
        raise FileNotFoundError(f"Missing base model: {args.pretrained_model}")
    if not args.train_data_dir.exists():
        raise FileNotFoundError(f"Missing train data dir: {args.train_data_dir}")
    if not args.reg_data_dir.exists():
        raise FileNotFoundError(f"Missing reg data dir: {args.reg_data_dir}")

    train_count = count_images(args.train_data_dir)
    reg_count = count_images(args.reg_data_dir)

    if train_count == 0:
        raise RuntimeError(f"No training images found in: {args.train_data_dir}")
    if reg_count == 0:
        raise RuntimeError(f"No regularization images found in: {args.reg_data_dir}")

    print(f"[dataset] train_images={train_count} reg_images={reg_count}")


def main() -> int:
    args = parse_args()
    if args.dataset_manifest_out is None:
        args.dataset_manifest_out = args.output_dir / "dataset_manifest.json"

    ensure_dependencies(skip_install=args.skip_install)
    validate_inputs(args)

    args.output_dir.mkdir(parents=True, exist_ok=True)
    args.logging_dir.mkdir(parents=True, exist_ok=True)

    if not args.skip_auto_caption:
        run_auto_caption(args)

    run_dataset_manifest(args)

    write_dataset_config(args.dataset_config, args)

    cmd = build_training_command(args)
    run(cmd)

    copy_outputs_to_comfyui(args)

    print("[done] LoRA v3 training pipeline complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
