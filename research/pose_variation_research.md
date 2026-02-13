# Pose Variation + Face Consistency Research (2026-02-11)

## KEY DISCOVERY: image_kps Input
ApplyInstantID has an `image_kps` optional input.
- Main image input = face identity (reference photo)
- image_kps input = pose/angle (separate image with desired pose)
- This decouples identity from pose completely

## ApplyInstantIDAdvanced Parameters
| Parameter | Default | Range | Purpose |
|-----------|---------|-------|---------|
| ip_weight | 0.8 | 0-3.0 | Face identity strength |
| cn_strength | 0.8 | 0-10.0 | Pose/keypoint control strength |
| noise | 0.0 | 0-1.0 | Adds variation |

Lower cn_strength (0.4-0.6) = more pose freedom
Keep ip_weight at 0.7-0.8 for identity

## Body Pose Control
InstantID ControlNet only controls HEAD orientation.
For body pose: add second ControlNet (OpenPose or Depth)
- ControlNet Union ProMax (xinsir) = best single model for SDXL
- thibaud/controlnet-openpose-sdxl-1.0 = dedicated OpenPose

Combined strengths:
- InstantID cn_strength: 0.4-0.6 (face keypoints)
- OpenPose strength: 0.7-0.85 (body pose)

## FaceDetailer Settings (Post-Processing)
| Parameter | Value | Notes |
|-----------|-------|-------|
| denoise | 0.40-0.45 | Sweet spot for InstantID |
| bbox_crop_factor | 1.3 | NOT default 3.0 |
| feather | 16-32 | Blend zone |
| steps | 50 | Higher than gen steps |
| CFG | 5-8 | |
| bbox_detector | face_yolov8m.pt | |
| guide_size | 384 | Standard |

## Quality Thresholds
- >= 0.75: Excellent match
- 0.65-0.75: Good match (we're here at 0.70)
- 0.55-0.65: Moderate (review manually)
- < 0.55: Poor (discard)

## Prompt Engineering for SDXL Poses
Camera angles that work:
- "front view" / "three-quarter view" / "profile view"
- "from above" / "from below" / "eye level"
- "close-up" / "medium shot" / "full body shot"
- "selfie" / "over the shoulder" / "candid"

Rule: Don't combine contradictory terms (e.g., "from above" + "looking at viewer")

## Sources
- cubiq/ComfyUI_InstantID GitHub
- runcomfy.com ApplyInstantIDAdvanced docs
- CivitAI camera angles guide
- xinsir/controlnet-union-sdxl HuggingFace
- ltdrdata/ComfyUI-Impact-Pack GitHub
- CivitAI FaceDetailer guide
- cubiq/ComfyUI_FaceAnalysis GitHub
