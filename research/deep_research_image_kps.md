# image_kps Pose Decoupling — Deep Research (2026-02-11)

## KEY FINDING: image_kps is the #1 most underutilized feature we have

## How It Works
- ApplyInstantIDAdvanced has an `image_kps` input
- When connected, it takes **pose/head angle** from one image and **identity** from another
- Only controls **5 facial keypoints** (eyes, nose, mouth corners) = head orientation
- Does NOT control body pose (need separate ControlNet for that)

## How to Use
```
[Identity Photo] → image input → ApplyInstantIDAdvanced
[Pose Photo]     → image_kps input → ApplyInstantIDAdvanced
```
- Pose photo can be ANY person — only keypoints are extracted
- Identity comes from the main `image` input only

## What It Controls vs Doesn't
- CONTROLS: Head angle (left/right/up/down), face orientation, 3/4 view
- DOES NOT CONTROL: Body pose, arms, legs, sitting/standing

## For Full Body Pose Control: Stack ControlNets
Use `ApplyInstantIDControlNet` node to add DWPose/OpenPose on top:
```
ApplyInstantIDAdvanced → ApplyInstantIDControlNet → KSampler
                              ↑
                    DWPose ControlNet + Pose Reference
```

Three-layer approach:
1. InstantID IP-Adapter → identity
2. image_kps → head orientation
3. DWPose ControlNet → full body pose

## Recommended Settings for Combined Workflow
- ip_weight: 0.6-0.8 (identity)
- cn_strength: 0.6-0.8 (facial keypoint pose)
- Additional ControlNet strength: 0.5-0.8 (body pose)
- noise: 0.2-0.4 (prevents artifacts from competing signals)
- CFG: 4-5 (critical — higher causes artifacts with InstantID)

## Action Items for V3
1. Collect 7 face-angle reference photos (front, left profile, right profile, looking up, looking down, 3/4 left, 3/4 right) — can be stock photos of anyone
2. Feed different image_kps for each prompt to break "same pose" problem
3. Consider adding DWPose ControlNet for full body shots
4. Required node: comfyui_controlnet_aux (by Fannovel16) for DWPose preprocessor

## FaceKeypointsPreprocessor Node
- Alternative: manually draw the 5 keypoints instead of using a reference photo
- CTRL+DRAG to pan, CTRL+WHEEL to zoom, ALT+WHEEL to adjust point spacing
- Can import 3D KPS positions and rotate/scale them
