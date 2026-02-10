#!/usr/bin/env python3
"""Track RunPod usage sessions and aggregate cost over time."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


@dataclass
class SessionState:
    session_id: str
    start: str
    activity: str
    gpu: str
    rate_per_hr: float


def now_utc() -> datetime:
    return datetime.now(timezone.utc)


def iso(dt: datetime) -> str:
    return dt.replace(microsecond=0).isoformat().replace("+00:00", "Z")


def parse_iso(value: str) -> datetime:
    if value.endswith("Z"):
        value = value[:-1] + "+00:00"
    return datetime.fromisoformat(value).astimezone(timezone.utc)


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return rows


def next_session_id(log_rows: list[dict[str, Any]], start_dt: datetime) -> str:
    date_prefix = start_dt.strftime("%Y-%m-%d")
    existing = [
        row.get("session_id", "")
        for row in log_rows
        if str(row.get("session_id", "")).startswith(date_prefix + "_")
    ]
    max_idx = 0
    for session_id in existing:
        try:
            max_idx = max(max_idx, int(session_id.rsplit("_", 1)[1]))
        except Exception:  # noqa: BLE001
            continue
    return f"{date_prefix}_{max_idx + 1:03d}"


def load_state(path: Path) -> SessionState | None:
    if not path.exists():
        return None
    data = json.loads(path.read_text(encoding="utf-8"))
    return SessionState(
        session_id=data["session_id"],
        start=data["start"],
        activity=data["activity"],
        gpu=data["gpu"],
        rate_per_hr=float(data["rate_per_hr"]),
    )


def save_state(path: Path, state: SessionState) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state.__dict__, indent=2), encoding="utf-8")


def clear_state(path: Path) -> None:
    if path.exists():
        path.unlink()


def action_start(args: argparse.Namespace, log_path: Path, state_path: Path) -> int:
    state = load_state(state_path)
    if state is not None:
        print(
            f"[FAIL] Active session already running: {state.session_id} "
            f"(activity={state.activity}, start={state.start}). Stop it first."
        )
        return 1

    rows = read_jsonl(log_path)
    start_dt = now_utc()
    session_id = next_session_id(rows, start_dt)
    new_state = SessionState(
        session_id=session_id,
        start=iso(start_dt),
        activity=args.activity,
        gpu=args.gpu,
        rate_per_hr=float(args.rate_per_hr),
    )
    save_state(state_path, new_state)
    print(f"[ok] Started session {session_id} activity={args.activity} rate=${args.rate_per_hr:.2f}/hr")
    return 0


def action_stop(args: argparse.Namespace, log_path: Path, state_path: Path) -> int:
    state = load_state(state_path)
    if state is None:
        print("[FAIL] No active session found. Start one first.")
        return 1

    start_dt = parse_iso(state.start)
    end_dt = now_utc()
    duration_min = max(0.0, (end_dt - start_dt).total_seconds() / 60.0)
    cost = (duration_min / 60.0) * state.rate_per_hr

    row = {
        "session_id": state.session_id,
        "start": state.start,
        "end": iso(end_dt),
        "duration_min": round(duration_min, 2),
        "activity": state.activity,
        "cost_usd": round(cost, 4),
        "gpu": state.gpu,
        "rate_per_hr": state.rate_per_hr,
    }
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(row) + "\n")

    clear_state(state_path)
    print(
        f"[ok] Stopped session {state.session_id}: duration={duration_min:.2f} min "
        f"cost=${cost:.4f} activity={state.activity}"
    )
    return 0


def action_report(args: argparse.Namespace, log_path: Path, state_path: Path) -> int:
    rows = read_jsonl(log_path)
    total_min = sum(float(row.get("duration_min", 0.0)) for row in rows)
    total_cost = sum(float(row.get("cost_usd", 0.0)) for row in rows)

    by_activity: dict[str, dict[str, float]] = {}
    for row in rows:
        activity = str(row.get("activity", "unknown"))
        bucket = by_activity.setdefault(activity, {"sessions": 0.0, "minutes": 0.0, "cost": 0.0})
        bucket["sessions"] += 1.0
        bucket["minutes"] += float(row.get("duration_min", 0.0))
        bucket["cost"] += float(row.get("cost_usd", 0.0))

    print("=== RunPod Cost Report ===")
    print(f"Total sessions: {len(rows)}")
    print(f"Total hours: {total_min / 60.0:.2f}")
    print(f"Total cost: ${total_cost:.2f}")
    print("By activity:")
    for activity, bucket in sorted(by_activity.items(), key=lambda item: item[0]):
        print(
            f"  {activity}: {int(bucket['sessions'])} sessions, "
            f"{bucket['minutes'] / 60.0:.2f} hrs, ${bucket['cost']:.2f}"
        )

    active = load_state(state_path)
    if active is not None:
        print(
            f"[warn] Active session not yet stopped: {active.session_id} "
            f"(activity={active.activity}, start={active.start})"
        )

    if args.json:
        payload = {
            "total_sessions": len(rows),
            "total_hours": total_min / 60.0,
            "total_cost_usd": total_cost,
            "by_activity": by_activity,
            "active_session": active.__dict__ if active else None,
        }
        print(json.dumps(payload, indent=2))
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Track RunPod session cost.")
    parser.add_argument("--action", choices=["start", "stop", "report"], required=True)
    parser.add_argument("--activity", default="unspecified", help="Session activity tag for start action.")
    parser.add_argument("--gpu", default="RTX 4090")
    parser.add_argument("--rate-per-hr", type=float, default=0.60)
    parser.add_argument("--log-file", type=Path, default=Path("tools/cost_log.jsonl"))
    parser.add_argument("--state-file", type=Path, default=Path("tools/.cost_session_state.json"))
    parser.add_argument("--json", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    log_path = args.log_file.resolve()
    state_path = args.state_file.resolve()

    if args.action == "start":
        return action_start(args, log_path, state_path)
    if args.action == "stop":
        return action_stop(args, log_path, state_path)
    return action_report(args, log_path, state_path)


if __name__ == "__main__":
    raise SystemExit(main())

