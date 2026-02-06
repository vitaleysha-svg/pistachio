# Pistachio - Complete Setup Checklist

## TECH STUFF (Do Now - One Time Setup)

### 1. RunPod Account
- [ ] Go to runpod.io and sign up
- [ ] Add payment method (credit card)
- [ ] Deposit $10 (you get $5-$500 bonus)

### 2. Deploy ComfyUI on RunPod
- [ ] Go to Pods > Deploy
- [ ] Select template: **"ComfyUI"**
- [ ] Select GPU: **RTX 4090** (~$0.34/hr on Community Cloud)
- [ ] Set Container Disk: **30GB** (need space for models)
- [ ] Set Volume Disk: **50GB** (persistent storage)
- [ ] Click Deploy (first boot ~30 min)

### 3. Run Pistachio Setup Script
- [ ] Once pod is running, click **Connect** > **Terminal**
- [ ] Copy+paste the ENTIRE contents of `tools/runpod-comfyui-setup.sh`
- [ ] Wait for all downloads to finish (~15-20 min)
- [ ] Script downloads: SDXL base, InstantID, IP-Adapter FaceID, InsightFace

### 4. Upload Midjourney Hero Images
- [ ] In RunPod terminal, navigate to `input/pistachio_reference/`
- [ ] Use RunPod's file manager or `wget` to upload your best Midjourney images
- [ ] Need at least 1 hero image, ideally 3-5 different angles

### 5. Build ComfyUI Workflow
- [ ] Open ComfyUI in browser (Connect > HTTP Service port 8188)
- [ ] Load SDXL checkpoint
- [ ] Add InstantID + IP-Adapter FaceID nodes
- [ ] Connect your reference face image
- [ ] Settings per blueprint:
  - IP-Adapter weight: 0.8-1.0
  - ControlNet strength: 0.8-1.0
  - CFG Scale: 7.5-12.0
  - Steps: 25-40
  - Sampler: DPM++ 2M Karras
- [ ] Generate first test image
- [ ] If face consistency > 85%, proceed with batch generation
- [ ] If face consistency < 85%, proceed to LoRA training (Step 6)

### 6. LoRA Training (Only If Needed)
- [ ] In RunPod terminal, paste contents of `tools/runpod-lora-training-setup.sh`
- [ ] Upload 15-30 captioned images to `training_data/pistachio/img/`
- [ ] Create .txt caption file for each image (trigger word: pistachio_character)
- [ ] Run: `bash /workspace/train_pistachio_lora.sh`
- [ ] Wait ~30-60 min for training
- [ ] Copy output LoRA to ComfyUI's `models/loras/` directory

### 7. Batch Generate Content Library
- [ ] Generate 50+ images with consistent face (different poses, outfits, settings)
- [ ] Use the 8 prompt templates from the Operations Manual (Section 5)
- [ ] Download all images to your local machine
- [ ] STOP YOUR RUNPOD POD when done (saves money!)

---

## MANUAL STUFF (Do After Tech Setup)

### Platform Accounts
- [x] Instagram: @itsamiranoor (already created per blueprint)
- [x] Fanvue: itsamiranoor (already created per blueprint)
- [x] Email: amiranoor741@outlook.com (already created per blueprint)
- [ ] ManyChat: Sign up at manychat.com, connect Instagram

### Instagram Setup
- [ ] Switch to Creator account
- [ ] Upload hero image as profile photo
- [ ] Write bio (150 chars, lowercase, mysterious, include link)
- [ ] Add Fanvue link (via Linktree or direct)
- [ ] Wait 24-48 hours before posting (account warm-up)

### Fanvue Setup
- [ ] Upload hero image as profile photo
- [ ] Write bio (200-300 chars)
- [ ] Set pricing: $9.99/month base subscription
- [ ] Set up PPV pricing tiers ($5-50 per piece)
- [ ] Complete ID verification (KYC)
- [ ] Connect payment method, set weekly payout

### ManyChat Setup
- [ ] Connect Instagram account
- [ ] Create Welcome Flow (triggers on new follow):
  - Wait 1 min delay
  - Send: "hey :) thanks for the follow! how'd you find me?"
- [ ] Create Comment Triggers:
  - "link" / "more" -> sends DM with next step
  - 30-60 second delay before responding
- [ ] Create Keyword Flows:
  - "link" -> Fanvue link
  - "hey" / "hi" -> conversation starter
  - "more" -> tease content, ask for email
- [ ] Test from a second account

### Content Upload
- [ ] Upload generated images to Fanvue (tiered: free teasers vs paid)
- [ ] Schedule first 3 Instagram posts
- [ ] Create first batch of Stories (3-5)
- [ ] Set up content calendar per blueprint (Section 9)

---

## COST SUMMARY

| Item | Cost | Frequency |
|------|------|-----------|
| Midjourney | $30/month | Monthly |
| RunPod GPU | ~$10-20/session | As needed |
| ManyChat | $15/month (free to start) | Monthly |
| Fanvue | Free (20% of earnings) | Per sale |
| Instagram | Free | - |
| **Total startup** | **~$50-75** | **Month 1** |

---

## IMPORTANT REMINDERS
- ALWAYS stop RunPod pods when not using them ($0.34/hr adds up)
- ALWAYS use "Made with AI" label on Instagram (mandatory 2026)
- Keep IG content clean (suggestive OK, explicit NO)
- Save explicit content for Fanvue only
- Username has no numbers (algorithm penalty)
- Don't DM too aggressively on IG (spam flags)
