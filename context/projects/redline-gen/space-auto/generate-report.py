from fpdf import FPDF
import os

class Report(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(220, 50, 50)
        self.cell(0, 8, "REDLINE GEN  |  CAMPAIGN PERFORMANCE REPORT", align="R", new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(220, 50, 50)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(4)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, "RedLine Gen  |  Confidential  |  Page %d/{nb}" % self.page_no(), align="C")

    def stitle(self, t):
        self.set_font("Helvetica", "B", 14)
        self.set_text_color(30, 30, 30)
        self.cell(0, 10, t, new_x="LMARGIN", new_y="NEXT")
        self.ln(2)

    def sub(self, t):
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(60, 60, 60)
        self.cell(0, 8, t, new_x="LMARGIN", new_y="NEXT")
        self.ln(1)

    def txt(self, t):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(50, 50, 50)
        self.multi_cell(0, 5.5, t, new_x="LMARGIN", new_y="NEXT")
        self.ln(2)

    def btxt(self, t):
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(50, 50, 50)
        self.multi_cell(0, 5.5, t, new_x="LMARGIN", new_y="NEXT")
        self.ln(1)

    def bul(self, t):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(50, 50, 50)
        self.multi_cell(0, 5.5, "  - " + t, new_x="LMARGIN", new_y="NEXT")

    def tbl(self, headers, data, cw=None):
        if cw is None:
            cw = [190 // len(headers)] * len(headers)
        self.set_font("Helvetica", "B", 8)
        self.set_fill_color(40, 40, 40)
        self.set_text_color(255, 255, 255)
        for i, h in enumerate(headers):
            self.cell(cw[i], 7, h, border=1, fill=True, align="C")
        self.ln()
        self.set_font("Helvetica", "", 8)
        self.set_text_color(50, 50, 50)
        fill = False
        for row in data:
            if fill:
                self.set_fill_color(245, 245, 245)
            else:
                self.set_fill_color(255, 255, 255)
            for i, c in enumerate(row):
                self.cell(cw[i], 6, str(c), border=1, fill=True, align="C")
            self.ln()
            fill = not fill
        self.ln(3)

    def vbox(self, title, items, color):
        r, g, b = color
        self.set_fill_color(r, g, b)
        self.rect(10, self.get_y(), 190, 6, "F")
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(255, 255, 255)
        self.cell(190, 6, title, align="C", new_x="LMARGIN", new_y="NEXT")
        self.set_text_color(50, 50, 50)
        self.set_font("Helvetica", "", 9)
        for item in items:
            self.ln(1)
            self.cell(6, 5, "-")
            self.multi_cell(180, 5, item, new_x="LMARGIN", new_y="NEXT")
        self.ln(4)


pdf = Report()
pdf.alias_nb_pages()
pdf.set_auto_page_break(auto=True, margin=20)

# COVER
pdf.add_page()
pdf.ln(40)
pdf.set_font("Helvetica", "B", 28)
pdf.set_text_color(220, 50, 50)
pdf.cell(0, 15, "SPACE AUTO GROUP", align="C", new_x="LMARGIN", new_y="NEXT")
pdf.set_font("Helvetica", "", 16)
pdf.set_text_color(80, 80, 80)
pdf.cell(0, 10, "Campaign Performance Report", align="C", new_x="LMARGIN", new_y="NEXT")
pdf.ln(5)
pdf.set_font("Helvetica", "", 12)
pdf.cell(0, 8, "Reporting Period: February 1 - 7, 2026 (7 Days)", align="C", new_x="LMARGIN", new_y="NEXT")
pdf.cell(0, 8, "With 30-Day Trend Comparison (Jan 8 - Feb 6)", align="C", new_x="LMARGIN", new_y="NEXT")
pdf.ln(20)
pdf.set_draw_color(220, 50, 50)
pdf.line(60, pdf.get_y(), 150, pdf.get_y())
pdf.ln(10)
pdf.set_font("Helvetica", "", 11)
pdf.set_text_color(100, 100, 100)
pdf.cell(0, 7, "Prepared by: RedLine Gen", align="C", new_x="LMARGIN", new_y="NEXT")
pdf.cell(0, 7, "Date: February 7, 2026", align="C", new_x="LMARGIN", new_y="NEXT")
pdf.cell(0, 7, "Classification: Confidential", align="C", new_x="LMARGIN", new_y="NEXT")

# EXECUTIVE SUMMARY
pdf.add_page()
pdf.stitle("EXECUTIVE SUMMARY")
pdf.txt("This report analyzes Space Auto Group's Meta advertising campaigns for the 7-day period of February 1-7, 2026, with trend comparisons against the prior 30-day window.")

pdf.sub("7-Day Performance Snapshot")
pdf.tbl(
    ["Metric", "7-Day", "30-Day", "Trend"],
    [
        ["Total Spend", "$281.45", "$1,685.50", "-"],
        ["Total Leads", "27", "153", "-"],
        ["Avg CPL", "$10.42", "$11.02", "Improved"],
        ["Reach", "6,341", "24,745", "-"],
        ["Frequency", "1.47", "2.21", "Improved"],
        ["CPM", "$30.18", "$30.83", "Stable"],
        ["CPC", "$1.02", "$1.29", "Improved"],
        ["CTR (link)", "2.97%", "2.40%", "Improved"],
    ],
    [50, 40, 40, 40]
)
pdf.txt("Key takeaway: CPL improved from $11.02 to $10.42. Frequency dropped from 2.21 to 1.47 (less fatigue). CTR improved from 2.40% to 2.97%. The reduced budget is producing more efficient results.")

# AD PERFORMANCE
pdf.add_page()
pdf.stitle("AD PERFORMANCE RANKING (7 DAYS)")
pdf.sub("All Active Ads - Ranked by Cost Per Lead")
pdf.tbl(
    ["Ad", "Leads", "CPL", "Reach", "CPM", "CTR", "Spend"],
    [
        ["Testimonial S5", "10", "$9.27", "2,295", "$32.89", "2.27%", "$92.66"],
        ["Luxury Carousel", "6", "$9.31", "2,685", "$15.16", "2.66%", "$55.84"],
        ["Fake Prices", "9", "$10.06", "1,630", "$42.72", "4.01%", "$90.52"],
        ["Dont Buy New", "1", "$6.44", "133", "$42.65", "2.65%", "$6.44"],
        ["Fast Actions", "1", "$35.46", "393", "$68.19", "4.62%", "$35.46"],
        ["Subprime Carousel", "0", "-", "32", "$15.76", "6.06%", "$0.52"],
        ["Why Us", "0", "-", "2", "$5.00", "-", "$0.01"],
    ],
    [40, 16, 18, 20, 22, 18, 22]
)

pdf.sub("Quality Scores (Meta)")
pdf.tbl(
    ["Ad", "Engagement", "Conversion", "Signal"],
    [
        ["Testimonial S5", "Above Avg", "Above Avg", "STRONG"],
        ["Fake Prices", "Above Avg", "Above Avg", "STRONG"],
        ["Fast Actions", "Above Avg", "Average", "MIXED"],
        ["Luxury Carousel", "Above Avg", "Average", "GOOD"],
        ["Dont Buy New", "-", "-", "WEAK"],
        ["Why Us", "-", "-", "DEAD"],
    ],
    [50, 40, 40, 30]
)

# TREND
pdf.add_page()
pdf.stitle("30-DAY VS 7-DAY TREND ANALYSIS")
pdf.sub("CPL Trend Comparison")
pdf.tbl(
    ["Ad", "30-Day CPL", "7-Day CPL", "Change", "Trend"],
    [
        ["Testimonial S5", "$9.07", "$9.27", "+2.2%", "STABLE"],
        ["Luxury Carousel", "$9.70", "$9.31", "-4.0%", "IMPROVING"],
        ["Fake Prices", "$7.80-12.12", "$10.06", "-", "STABLE"],
        ["Fast Actions", "$15.82", "$35.46", "+124%", "COLLAPSING"],
        ["Dont Buy New", "$22.47", "$6.44*", "-", "UNRELIABLE"],
        ["Why Us", "$11.43", "N/A", "-", "DEAD"],
    ],
    [38, 30, 30, 25, 30]
)
pdf.txt("* Dont Buy New: $6.44 CPL on only 1 lead / 133 reach in 7 days. Facebook barely serves this ad. The 30-day CPL of $22.47 is the true indicator.")

pdf.sub("CPM Trend")
pdf.tbl(
    ["Ad", "30-Day CPM", "7-Day CPM", "Signal"],
    [
        ["Luxury Carousel", "$16.40", "$15.16", "Most efficient"],
        ["Testimonial S5", "$28.12", "$32.89", "Moderate"],
        ["Fake Prices", "$28-45", "$42.72", "Expensive but converts"],
        ["Dont Buy New", "$48.19", "$42.65", "Expensive, low delivery"],
        ["Fast Actions", "$67.86", "$68.19", "WORST - FB penalizing"],
    ],
    [42, 35, 35, 55]
)

# KILL / KEEP / SCALE
pdf.add_page()
pdf.stitle("ACTION PLAN: KILL / KEEP / SCALE")

pdf.vbox("SCALE - Increase Budget", [
    "Testimonial S5 | 10 leads @ $9.27 CPL | Engagement+Conversion: Above Avg | 37% of all leads. Consistent 30-day performer. This is the engine.",
    "Luxury Carousel W/Monthly | 6 leads @ $9.31 CPL | CPM $15.16 (LOWEST) | CPC $0.57 (LOWEST) | Most cost-efficient ad in the account.",
], (34, 139, 34))

pdf.vbox("KEEP - Monitor Weekly", [
    "Video - Fake Prices | 9 leads @ $10.06 CPL | CTR 4.01% (highest) | Engagement+Conversion: Above Avg | Strong but CPM $42.72 is high. Watch for CPL creep.",
], (30, 100, 200))

pdf.vbox("KILL - Turn Off Immediately", [
    "Video - Fast Actions | 1 lead @ $35.46 CPL | CPM $68.19 (HIGHEST) | Was $15.82 CPL 30-day, now $35.46 = +124%. Deteriorating rapidly.",
    "Video - Dont Buy New | 1 lead, 133 reach in 7 days. FB barely shows it. 30-day CPL $22.47.",
    "Video - Why Us | 0 leads, 2 impressions. Facebook refuses to deliver. Dead.",
    "Subprime Carousel (ForceSpend) | 0 leads, 32 reach. No traction.",
    "ForceSpend Ad Set | Kill entirely. Highest CPM, fights algorithm.",
], (200, 40, 40))

# BUDGET REALLOCATION
pdf.add_page()
pdf.stitle("BUDGET REALLOCATION PLAN")
pdf.sub("Current vs Recommended")
pdf.tbl(
    ["Ad Set", "Current", "Proposed", "Rationale"],
    [
        ["ForceSpend", "$11/day", "$0 KILL", "Fights algorithm, worst CPM"],
        ["Prime/Videos", "$11/day", "$11/day", "Remove losers, keep winners"],
        ["SP/Carousels", "$11/day", "$15/day", "Best performer, more budget"],
        ["Retargeting", "$0 (OFF)", "$7/day ON", "Capture warm LP visitors"],
        ["TOTAL", "$33/day", "$33/day", "Same spend, better allocation"],
    ],
    [40, 28, 28, 62]
)
pdf.txt("Same daily spend ($33/day) but redirected from waste to winners. Projected: 35-40 leads/week at $8-9 CPL vs current 27 leads/week at $10.42 CPL.")

# NEW CREATIVE
pdf.add_page()
pdf.stitle("NEW CREATIVE STRATEGY")
pdf.sub("What Works (Patterns from Data)")
pdf.bul("Testimonial/social proof = lowest CPL with volume")
pdf.bul("Carousel + monthly payment = lowest CPM, best efficiency")
pdf.bul("Price transparency hooks (Fake Prices) = highest CTR")
pdf.ln(3)

pdf.sub("New Video Scripts - Car Sourcing Angle (15-20 sec each)")
pdf.txt("These go into the Prime/Videos ad set as replacements for the killed ads. All shot on iPhone, 9:16 vertical, CapCut captions, no music.")

pdf.btxt('Script 1: "Stop Settling" (18 sec)')
pdf.txt('SCENE 1 (0-3s): Outside, standing in front of lot. Handheld, chest-up shot.\nLine: "If you are tired of settling for whatever is on the lot - I got you."\nDirection: Already looking at camera. Confident, not yelling. "I got you" is the anchor - say it directly.\n\nSCENE 2 (3-12s): Same shot, no cut. One step forward.\nLine: "You tell us the car you want - make, model, color, budget - and we go find it. That is literally what we do."\nDirection: Tick off "make, model, color, budget" on fingers. On "literally what we do" - palm to chest.\n\nSCENE 3 (12-18s): Same shot.\nLine: "Fill out the form. Tell us your dream car. We handle the rest."\nDirection: Point down (toward link). Calm close. Eye contact hold 1 beat, cut.\nText overlay: "We find YOUR car" at 4-second mark, lower third, 3 seconds.')

pdf.btxt('Script 2: "You Have Been Lied To" (17 sec)')
pdf.txt('SCENE 1 (0-4s): Inside office or car, close-up shoulders and up. Camera on surface, not held.\nLine: "You have been lied to about buying a car and it is time someone told you the truth."\nDirection: Dead serious face. Lean in slightly. This is the pattern interrupt - no smile.\n\nSCENE 2 (4-12s): Same shot, no cut.\nLine: "Most dealers only sell what is on their lot. You show up, they push whatever they have. We do the opposite - you tell US what you want, and we go find it."\nDirection: Dismissive wave on "push whatever they have." Point at camera on "you tell US."\n\nSCENE 3 (12-17s): Same shot.\nLine: "Fill out the form. Tell us exactly what you want. We will find it."\nDirection: Nod on "we will find it." Confident. Cut.')

pdf.btxt('Script 3: "The Secret" (Testimonial Format, 20 sec)')
pdf.txt('SCENE 1 (0-5s): Customer in driver seat of car Space Auto found, OR owner standing next to a sold car.\nLine: "[Name] wanted a specific car. Looked for 2 months on their own. Every dealer had the same junk."\nDirection: If customer - let them say it naturally. If owner - tell the story standing next to the car.\n\nSCENE 2 (5-14s): Same shot OR cut to B-roll of the car (3 sec walk around) with voiceover.\nLine: "They told us exactly what they wanted. We found it in [X] days. Done."\nDirection: On "Done" - pat the car or slap the roof. The physical contact with the car = proof.\n\nSCENE 3 (14-20s): Back to face, close-up.\nLine: "Want us to find yours? Link is right there."\nDirection: Point down. Casual, like "your turn." Cut.')

pdf.btxt('Script 4: "Tax Season" (16 sec) - Add to SP/Carousels ad set')
pdf.txt('NOTE: This is NOT a new campaign. Add this as a new ad inside SP/Carousels (your best ad set).\n\nSCENE 1 (0-4s): Outside or inside. Handheld close-up.\nLine: "Tax season is here. Here is how to turn your refund into the car you actually want."\nDirection: Upbeat but not cheesy. "Actually want" is the emphasis.\n\nSCENE 2 (4-12s): Same shot.\nLine: "Instead of going to a dealer and picking from whatever they have - tell us your budget and dream car. We source it for you."\nDirection: On "whatever they have" - shake head. On "we source it" - thumb to chest.\n\nSCENE 3 (12-16s):\nLine: "Your refund. Your car. Fill out the form."\nDirection: Three short punchy sentences. Point down on "fill out the form." Cut.\nText overlay: "Tax Refund + Dream Car" at 5-second mark.')

# RETARGETING SCRIPTS
pdf.add_page()
pdf.stitle("RETARGETING VIDEO SCRIPTS (15-20 SEC)")
pdf.txt("Target: People who visited the landing page but did not convert. They already know Space Auto. These scripts overcome the specific objection that stopped them. Budget: $7/day. All scripts 15-20 seconds max.")
pdf.ln(1)

pdf.sub('Script 1: "You Didn\'t Finish" (Objection Crusher) - 18 sec')
pdf.btxt("Scene 1 - Hook (0-3s)")
pdf.txt('Setting: Outside, in front of lot. Handheld, chest-up. Slight natural camera shake (NOT tripod).\nLine: "Hey - you were just looking at our page, right?"\nDirection: Head tilted. Say it like you ran into someone you recognized. Not aggressive.')

pdf.btxt("Scene 2 - Proof + Acknowledge (3-12s) - Same shot, no cut")
pdf.txt('Line: "We found 3 cars this week for people who filled out that form. One guy wanted a white Camry under 15K - had it for him in 4 days."\nDirection: Hold up 3 fingers on "3 cars" then drop naturally. Matter of fact, not bragging.\nText overlay: "We found 3 cars this week" - bold white, lower third, 3 seconds.')

pdf.btxt("Scene 3 - CTA (12-18s) - Same shot")
pdf.txt('Line: "Tell us what car you want. Worst case, you find out what is available. That is it."\nDirection: Small shrug on "That is it." Hold eye contact 1 beat, cut. No outro graphic.')
pdf.ln(1)

pdf.sub('Script 2: "The One That Got Away" (Urgency/FOMO) - 17 sec')
pdf.btxt("Scene 1 - Hook (0-3s)")
pdf.txt('Setting: INSIDE office. Sitting at desk or leaning on counter. Camera on surface at eye level, NOT held. Feels like a FaceTime.\nLine: "Real quick - let me tell you what happened yesterday."\nDirection: Lean forward. Half-smile. Indoor setting = different from cold ads (which are outdoor).')

pdf.btxt("Scene 2 - Story (3-12s) - Same shot, no cut, entire video is one take")
pdf.txt('Line: "Guy wanted a Honda Ridgeline, black, under 20K. We found two options. He waited ONE day to decide. Both got sold. Gone."\nDirection: Tick off specs on fingers. Slow down on "waited ONE day." Say "Both got sold. Gone." FLAT and dead serious. Pause after "Gone."')

pdf.btxt("Scene 3 - CTA (12-17s) - Same shot")
pdf.txt('Line: "Good cars move fast. Tell us what you want before someone else gets it."\nDirection: Snap fingers on "move fast." Point at camera on "tell us." Brief eye contact, cut.\nText overlay: "Good cars move FAST" at snap moment, center screen, 2 seconds.')
pdf.ln(1)

pdf.sub('Script 3: "Sourcing Story" (Social Proof) - 18 sec')
pdf.txt("Two versions depending on whether a real customer is available.")

pdf.btxt("Version A - Real Customer:")
pdf.txt('Scene 1 (0-7s): Customer sitting in driver seat of the car Space Auto found. Door open or window down.\nLine: "I looked for this car for 2 months. Every dealer had the same junk. Then I found Space Auto, told them what I wanted, and they had it in [X] days."\nDirection: Let them say it naturally. Don\'t over-script. The beats: frustration, then relief.\n\nScene 2 (7-13s): Same shot. Customer pats steering wheel or dashboard.\nLine: "I am sitting in it right now."\nDirection: Smile. Genuine. The car IS the proof.\n\nScene 3 (13-18s): Same shot, lean toward camera.\nLine: "Just tell them what you want. That is literally all I did."\nDirection: "Literally all I did" - hands up, palms out. Cut.')

pdf.btxt("Version B - Owner Tells It:")
pdf.txt('Scene 1 (0-5s): Owner standing next to a car on the lot. Medium shot.\nLine: "Customer came to us last week. Needed a [car], [color], under [price]."\nDirection: Hand on car roof. Matter of fact.\n\nScene 2 (5-13s): Same spot, lean on car.\nLine: "We found 3 options in 5 days. She drove off in exactly what she wanted."\nDirection: Hold up 3, then 5 fingers. On "exactly what she wanted" - point at camera.\n\nScene 3 (13-18s): One step toward camera.\nLine: "Stop thinking about it. Tell us what you want. We do the hard part."\nDirection: "Stop thinking" - flat, direct. "We do the hard part" - thumb to chest, slight smile. Cut.')
pdf.ln(1)

pdf.sub("Production Notes - All Scripts")
pdf.bul("15-20 seconds MAX. Sweet spot is 17-18 seconds. Never exceed 25.")
pdf.bul("Shoot all retargeting + cold traffic scripts in ONE afternoon (7 total)")
pdf.bul("iPhone, 9:16 vertical, NO background music (raw audio = authenticity)")
pdf.bul("CapCut captions: white text, black outline, auto-generated then proofread")
pdf.bul("First frame: person already looking at camera, mid-word. Not a posed smile.")

# SPEED TO LEAD
pdf.add_page()
pdf.stitle("CRITICAL: SPEED TO LEAD")
pdf.txt("Industry data shows conversion probability drops dramatically with delay:")
pdf.tbl(
    ["Response Time", "Conversion Rate", "Reality"],
    [
        ["< 1 minute", "391% higher", "IDEAL"],
        ["1-5 minutes", "Baseline", "Acceptable"],
        ["5-30 minutes", "50% drop", "Lead shopping competitors"],
        ["30+ minutes", "80% drop", "Lead is gone"],
    ],
    [45, 50, 65]
)
pdf.txt("Even the best ads mean nothing if leads are not called within 60 seconds. This is the single biggest lever for improving lead-to-sale conversion and is outside the scope of ad optimization.")

# STEP-BY-STEP IMPLEMENTATION GUIDE
pdf.add_page()
pdf.stitle("STEP-BY-STEP IMPLEMENTATION GUIDE")

pdf.sub("PHASE 1: Clean House (Today - 10 minutes in Ads Manager)")
pdf.tbl(
    ["Step", "Action", "Where"],
    [
        ["1", "Turn OFF Video - Fast Actions", "Prime/Videos ad set"],
        ["2", "Turn OFF Video - Dont Buy New", "Prime/Videos ad set"],
        ["3", "Turn OFF Video - Why Us", "Prime/Videos ad set"],
        ["4", "Turn OFF entire ForceSpend ad set", "Ad set level toggle"],
        ["5", "Verify 3 ads remain active", "See below"],
    ],
    [15, 100, 55]
)
pdf.txt("After Phase 1, only these ads should be running:\n- Testimonial S5 (in SP/Carousels) - your #1 performer\n- Luxury Carousel W/Monthly (in SP/Carousels) - lowest CPM\n- Video - Fake Prices (in Prime/Videos) - highest CTR")

pdf.sub("PHASE 2: Reallocate Budget (Today - 5 minutes)")
pdf.tbl(
    ["Step", "Action", "Detail"],
    [
        ["6", "Increase SP/Carousels budget", "$11/day -> $15/day"],
        ["7", "Keep Prime/Videos budget", "$11/day (now only Fake Prices)"],
        ["8", "Confirm daily spend", "$26/day across 2 ad sets"],
    ],
    [15, 100, 55]
)

pdf.sub("PHASE 3: Activate Retargeting (Today - 5 minutes)")
pdf.tbl(
    ["Step", "Action", "Detail"],
    [
        ["9", "Turn ON Warm-Retargeting-Website/LP", "Campaign level toggle"],
        ["10", "Set retargeting budget", "$7/day"],
        ["11", "Confirm new total daily spend", "$33/day ($15+$11+$7 = same as before)"],
    ],
    [15, 100, 55]
)

pdf.add_page()
pdf.stitle("STEP-BY-STEP (CONTINUED)")

pdf.sub("PHASE 4: Produce Retargeting Content (This Week)")
pdf.tbl(
    ["Step", "Action", "Detail"],
    [
        ["12", "Block 2-3 hours for video shoot", "One afternoon, all scripts"],
        ["13", "Shoot 3 retargeting scripts", "See Retargeting Scripts section"],
        ["14", "Edit in CapCut", "Add captions, NO music, export 9:16"],
        ["15", "Upload to retargeting campaign", "Add as new ads in retargeting"],
    ],
    [15, 100, 55]
)

pdf.sub("PHASE 5: New Cold Traffic Content (Next 2 Weeks)")
pdf.tbl(
    ["Step", "Action", "Detail"],
    [
        ["16", "Shoot 4 cold traffic video scripts", "See New Creative section"],
        ["17", "Upload car sourcing videos", "Add to Prime/Videos ad set"],
        ["18", "Upload Tax Season ad", "Add to SP/Carousels ad set (NOT new campaign)"],
        ["19", "Monitor 7 days", "Compare CPL to current $10.42 baseline"],
        ["20", "Review and adjust", "Kill anything above $15 CPL after 7 days"],
    ],
    [15, 100, 55]
)

pdf.txt("IMPORTANT: Tax season is NOT a new campaign. It goes into SP/Carousels as a new ad. Meta already has audience learning on that ad set - a new campaign would reset all optimization.")

pdf.sub("Targets After Implementation")
pdf.tbl(
    ["Metric", "Current", "Target", "Timeframe"],
    [
        ["CPL", "$10.42", "< $9.00", "2-3 weeks"],
        ["Frequency", "1.47", "< 2.0", "Ongoing"],
        ["CTR", "2.97%", "> 3.5%", "With new creative"],
        ["Leads/Week", "27", "35-40", "After budget reallocation"],
    ],
    [40, 35, 35, 55]
)

pdf.ln(10)
pdf.set_font("Helvetica", "I", 10)
pdf.set_text_color(128, 128, 128)
pdf.cell(0, 8, "Report prepared by RedLine Gen  |  February 7, 2026", align="C")

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "SpaceAuto-Report-Feb7-2026-v2.pdf")
pdf.output(out)
print(f"PDF saved to: {out}")
