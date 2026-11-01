"""Sends 30 realistic sample leads to the n8n webhook, one every 2 seconds.
Usage:  python3 send_leads.py "https://YOUR-N8N.app.n8n.cloud/webhook/lead-intake"
(Synthetic demo data: names, companies and numbers are made up.)
"""
import json, sys, time, urllib.request

LEADS = [
 # name, company, email, phone, message
 ("Jennifer Alvarez","Summit Ridge Realty","jennifer.alvarez@summitridgerealty.com","+1 (415) 555-0142",
  "Hi, we're a 12-agent brokerage and leads go cold because follow-up is manual. We need an AI voice agent that calls new inquiries within minutes and logs everything in our CRM. Budget is approved for Q4 and we'd like to start this month."),
 ("Marcus Whitfield","Whitfield & Cole Law","m.whitfield@whitfieldcole.law","+44 7700 900318",
  "Our intake process is a mess. We want a chatbot plus CRM integration to qualify enquiries before they reach a partner. We have budget set aside and need this live within two weeks, so it's fairly urgent."),
 ("Priya Raman","Northwind Analytics","priya.raman@northwindanalytics.io","+1 (646) 555-0177",
  "We run a B2B SaaS with about 40 demo requests a week. Looking for automation to score and route leads into HubSpot for our sales team. Budget is approved and we'd like to kick off within the next couple of weeks."),
 ("Daniel Okafor","Greenleaf Solar","daniel@greenleafsolar.co","+1 (512) 555-0190",
  "Need an AI agent that books site surveys from web enquiries. We're losing leads after hours. Budget approved, hoping to get going soon."),
 ("Sofia Marchetti","Bella Vita Dental","sofia@bellavitadental.com","+61 491 570 156",
  "Our front desk can't keep up with calls. Interested in a voice agent and CRM integration for appointment booking. We have budget ready and would like to begin this month."),
 ("Omar Al-Hashimi","Gulf Horizon Logistics","omar.alhashimi@gulfhorizon.ae","+971 50 482 7713",
  "We manage freight enquiries across email and WhatsApp. Looking for workflow automation connected to our CRM. Budget is approved and we'd like a working version soon."),
 ("Rachel Kim","PeakForm Fitness","rachel.kim@peakformfitness.com","+1 (303) 555-0124",
  "We have 5 gyms and trial sign-ups aren't followed up consistently. Want AI automation for outreach to new leads. Ready to pay for the right solution and hoping to get started soon."),
 ("Tobias Lindqvist","Nordic Fleet Services","tobias.lindqvist@nordicfleet.se","+46 70 555 01 83",
  "Urgent: our sales team needs lead qualification automated and pushed into the CRM. Budget confirmed by management, we want to start now."),
 ("Amelia Foster","Foster Home Insurance","amelia@fosterhomeinsurance.com","+44 7700 900654",
  "Looking for an AI voice agent to handle renewal reminders and quote follow-ups. We've got budget approved and aim to start this month."),

 ("Carlos Mendoza","Mendoza Roofing","carlos@mendozaroofing.com","+1 (305) 555-0166",
  "We get plenty of web enquiries but follow-up is slow. Curious whether an AI chatbot could help. What does something like that usually cost?"),
 ("Hannah Becker","Becker Design Studio","hannah@beckerdesign.studio","+49 151 5550 1234",
  "Thinking about CRM automation for our client onboarding. Not in a rush, just exploring options and would like to see examples."),
 ("Nathan Brooks","Brooks Mortgage Group","nbrooks@brooksmortgage.com","+1 (214) 555-0108",
  "We're evaluating automation for our loan officers' lead follow-up. Could you share a case study or two?"),
 ("Lena Petrova","Atlas Recruitment","lena.petrova@atlasrecruit.co.uk","+44 7700 900227",
  "We want an AI agent to pre-screen candidates by phone. Still comparing vendors and nothing is decided yet."),
 ("Jamal Peterson","Peterson Auto Group","jamal@petersonauto.com","+1 (404) 555-0139",
  "Interested in a voice assistant for our sales team to qualify test-drive requests. Planning for early next year."),
 ("Isabelle Dubois","Maison Dubois Boutique","isabelle@maisondubois.fr","+33 6 12 55 01 42",
  "We run an online boutique and want to automate customer enquiries. Is chatbot integration with Shopify something you do?"),
 ("Ethan Clarke","Clarke Property Management","ethan.clarke@clarkepm.com.au","+61 491 570 313",
  "Tenant enquiries are overwhelming our small team. We'd like to get something in place this month, but first want to understand the process."),
 ("Mei Lin Zhang","Bamboo Pediatrics","meilin@bamboopediatrics.com","+1 (206) 555-0151",
  "We're a small clinic and phone calls keep piling up. We've set aside some budget for next quarter and want to see what's possible."),
 ("Andrew Whitaker","Whitaker Wealth Partners","andrew@whitakerwealth.com","+1 (617) 555-0182",
  "CRM integration for our advisors is on our roadmap. Could we have an introductory call sometime in the coming weeks?"),
 ("Grace Nwosu","Nwosu Events","grace@nwosuevents.co.uk","+44 7700 900881",
  "Exploring a chatbot to handle wedding enquiries. Spend isn't finalised yet, so I'm just gathering information."),
 ("Victor Hugo Santos","Santos Imports","victor@santosimports.com.br","+55 11 95550 1177",
  "We'd like to understand how automation could reduce manual order follow-ups. Please send some details."),

 ("Tom Reilly","","tom.reilly88@gmail.com","","Saw your portfolio, nice work."),
 ("Alicia Grant","Grant Consulting","alicia@grantconsulting.net","","Just browsing for now, thanks."),
 ("Paul Henderson","","paul.henderson@outlook.com","","Do you offer any free resources?"),
 ("Yuki Tanaka","Tanaka Studio","yuki@tanakastudio.jp","+81 90 5550 1189","Hello, I came across your page. Could you tell me a bit about what you do?"),
 ("Brian O'Connell","","brian.oconnell@yahoo.com","","Student project, looking for ideas."),
 ("Natalie Rhodes","Rhodes & Co","natalie@rhodesandco.com","+1 (720) 555-0173","Not sure yet if this is relevant for us. Maybe later in the year."),
 ("Simon Duarte","","simon.duarte@proton.me","","Checking prices only."),
 ("Clara Jensen","Jensen Bakery","clara@jensenbakery.dk","","Hi, how does this work?"),
 ("Kevin Morales","","kevin.morales@icloud.com","","Random question, are you taking on new clients?"),
 ("Diane Foster","Foster Landscaping","diane@fosterlandscaping.com","+1 (919) 555-0165","Just saw your post, will get back to you if we need anything."),
]

# interleave hot / warm / cold so they arrive mixed
hot, warm, cold = LEADS[0:9], LEADS[9:20], LEADS[20:30]
order = []
for i in range(11):
    for grp in (hot, warm, cold):
        if i < len(grp): order.append(grp[i])

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit('Usage: python3 send_leads.py "<production webhook url>"')
    URL = sys.argv[1]
    total = len(order)
    for idx,(name,company,email,phone,msg) in enumerate(order, 1):
        body = {"name":name,"email":email,"phone":phone,"company":company,"message":msg}
        req = urllib.request.Request(URL, data=json.dumps(body).encode(),
              headers={"Content-Type":"application/json"}, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                print(f"[{idx:02d}/{total}] {name:<20} -> {r.status} {r.read().decode()[:90]}")
        except Exception as e:
            print(f"[{idx:02d}/{total}] {name:<20} -> ERROR {e}")
        time.sleep(2)
    print("Done.")
