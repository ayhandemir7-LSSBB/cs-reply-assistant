# M6 — Generic AI vs Canyon

Stronger product grounding. Still needs review.

Across five requests covering all four channels, the Canyon system provides more selected-product details traceable to the KB. Generic copy includes an unsupported 30% confidence statistic, an out-of-scope road model and unsupported rack/fender claims. However, the system still uses banned phrases, loses a range qualifier and misses email/Instagram length requirements. These examples support a grounding advantage, not publication readiness or universal superiority.

Reviewer: Codex qualitative review against the repository knowledge base; not blind, independent or a native-language review. No external product verification.

## Method

Five fixed requests covering three product families and all four channels; ten generations, one per arm per request. The original three pairs were preserved; newsletter and Instagram were appended in a second batch under the same model and source-file hashes.
The generic baseline uses the same API model, language, format instructions and accuracy guidance,
without company documents. Our arm uses the real generate_draft pipeline with company context,
brand rules and banned-phrase guidance. This tests the whole product package, not the KB alone.
The customer here is the marketing user requesting content, not a support-ticket sender.
This is an API baseline, not a test of the ChatGPT application. Temperature is 0.7;
generation order alternates. All outputs are retained verbatim, including weaknesses.
Automated checks measure house style and length, not truth, persuasiveness or native-language quality.
One sample per case is illustrative, not statistical proof. No independent blind review was conducted.

Model: gpt-4o-mini; date UTC: 2026-10-23T11:05:53.183079+00:00; status: complete.

## Review rubric

Review factual grounding (claims trace to the selected KB section; preserve model qualifiers),
useful specificity (features connected to relevant rider benefits), brand voice (direct, concise,
British English, category-appropriate) and brief/format adherence. For each dimension use
0 = fails, 1 = mixed, 2 = meets, with quotations and a KB reference. Do not hide invented claims
inside an aggregate score. Unsupported does not mean factually false; the KB itself needs review.
Scores and winner remain pending until evidence is reviewed; no LLM-as-judge scores are invented.

## 1. Gravel / linkedin

Request: Write a Canyon Bicycles linkedin marketing draft about gravel bikes. Topic: autumn weekend adventures on mixed terrain. Write in British English.

### Generic AI — verbatim

Canyon gravel bikes are designed for versatility, allowing riders to tackle everything from smooth tarmac to rugged off-road paths with ease. 

As autumn settles in, the allure of weekend adventures on mixed terrain becomes irresistible. Picture yourself cruising through vibrant foliage, the crunch of leaves under your wheels, and the crisp air invigorating your ride. Whether you're navigating winding forest trails or enjoying a scenic country road, our gravel bikes promise a smooth and exhilarating experience. 🍂 With their lightweight frames and robust tyres, they are perfect for those seeking both adventure and comfort.

Embrace the spirit of exploration this season and discover new routes that challenge your skills and ignite your passion for cycling. 🌟 It’s the perfect time to gather friends and make unforgettable memories on your Canyon gravel bike.

Join the adventure today!  
#GravelBiking #AutumnRides #CanyonAdventures

Automated checks: 138 words · house-style checks: needs review.

### Canyon system — verbatim

The Canyon Grizl CF SL 8 1by weighs just 9.5 kg (size M) and boasts an impressive tyre clearance of up to 50 mm. 🍂 As autumn sets in, it's the perfect time to embrace weekend adventures on mixed terrain. The Grizl is designed to handle everything from gravel roads to rugged trails, giving you the freedom to explore the great outdoors without limits.

With its lightweight carbon frame and versatile geometry, you’ll experience stability and confidence on descents and broken paths. Plus, the ample clearance allows you to ride at lower pressures for enhanced grip and comfort, making those long rides even more enjoyable. 

Get ready to discover new routes and create unforgettable memories this autumn. 

#GravelAdventure #ExploreMore #CanyonBikes

Automated checks: 120 words · house-style checks: needs review.

### Evidence review

- Grounding advantage: the system names the Grizl CF SL 8 1by and states '9.5 kg (size M)' and 'up to 50 mm'. Both match product_specs.md, section 'Gravel: Canyon Grizl CF SL 8 1by'. The size qualifier is preserved.
- The generic draft stays broad: 'lightweight frames and robust tyres' and a 'smooth and exhilarating experience'. Some general benefits overlap with the KB, so they are not automatically false, but it provides no selected-model specification to verify.
- Both connect to autumn adventures and use direct address. Brand-voice superiority is not established: both use generic promotional language, and the system says 'without limits', an overbroad promise worth editing.
- House style: both fail. Generic contains the banned phrase 'Whether you're'; system contains 'ready to'. Word counts pass at 138 and 120 respectively. The system is more specific, not publication-ready.

## 2. Road / email

Request: Write a Canyon Bicycles email marketing draft about road bikes. Topic: comfortable long-distance rides for your next big day out. Write in British English.

### Generic AI — verbatim

Subject: Discover Comfort on Long-Distance Rides  
Preview: Perfect road bikes for your next adventure.  

Dear Cyclist,  

When it comes to long-distance rides, comfort is key. Our Canyon road bikes, like the Endurace and Ultimate series, are designed to keep you fresh during those extended journeys. With a lightweight frame and endurance geometry, you’ll experience less fatigue and more enjoyment on your rides. 🚴‍♂️  

The Endurace model features a relaxed riding position, allowing for hours of comfortable cycling, while the Ultimate series combines aerodynamics with a cushioned ride, perfect for tackling any terrain. Plus, with wider tyre clearance, you can easily swap to comfort-oriented tyres for a smoother experience on varied surfaces. 🌄  

Explore our range today and find the perfect bike for your next big day out.  

Ride in comfort!  
The Canyon team

Automated checks: 134 words · house-style checks: needs review.

### Canyon system — verbatim

Subject: Comfort for Your Long Rides  
Preview: Enjoy the freedom of long-distance cycling.  
Hello,  

Ready for your next big adventure? Our Endurace range is designed for those long-distance rides where comfort meets performance. The carbon frame ensures you experience a lightweight and efficient ride, while the "Sport" geometry provides a more comfortable position, reducing strain on your neck and back.  

With the VCLS seatposts, you can enjoy a smooth ride that dampens vibrations, allowing you to focus on the miles ahead. Plus, with tyre clearance accommodating 32-40 mm, you can tackle rough and mixed roads with confidence. 🌄🚴‍♂️  

Discover the perfect bike for your next long day out.  
The Canyon team

Automated checks: 113 words · house-style checks: needs review.

### Evidence review

- Grounding advantage: the system uses Endurace carbon-frame, Sport geometry and VCLS seatpost details from product_specs.md, section 'Road: Canyon Endurace (range-level features)'. It avoids the unverified CF 7 specification.
- The generic email introduces the Ultimate series and claims it combines 'aerodynamics with a cushioned ride'. Ultimate is absent from the selected road product facts. Past brand examples are not evidence for current product specifications; these claims cannot be established from the selected KB.
- System weakness: 'tyre clearance accommodating 32-40 mm' loses the KB qualifier 'by version'. This may imply that every Endurace has the same clearance; a reviewer should restore the qualification.
- Format trade-off: generic is 134 words and passes the length check; the system is 113 words and fails the 120-word minimum. Generic uses banned 'journey' (inside 'journeys') and 'the ultimate'; the latter overlaps a real model name, illustrating possible false positives in substring-based checks. System has no banned-phrase hits.
- Both include Subject, Preview, greeting and the exact team sign-off. Generic adds 'Ride in comfort!' after its main call to action; CTA adherence requires human review. Verdict: better selected-product grounding from the system, but no clean format win.

## 3. Mountain / linkedin

Request: Write a Canyon Bicycles linkedin marketing draft about mountain bikes. Topic: confidence and control on technical trails. Write in British English.

### Generic AI — verbatim

Riders on the Canyon Spectral have reported a 30% increase in their confidence levels while tackling technical trails. 

Our mountain bikes are designed to provide unparalleled control, allowing you to navigate the most challenging terrains with ease. The Spectral’s low centre of gravity and advanced suspension system ensure that every twist and turn feels manageable, leaving you free to focus on the thrill of the ride. 🌲 Whether you're descending steep paths or tackling rocky sections, you'll feel an instant connection to the trail beneath you.

Experience the joy of conquering obstacles that once seemed insurmountable. With Canyon's precision engineering, you can push your limits and elevate your mountain biking adventures. 🚵‍♂️ 

Take your riding to the next level today.  
#CanyonBikes #MountainBiking #RideWithConfidence

Automated checks: 121 words · house-style checks: needs review.

### Canyon system — verbatim

The Spectral CF 8 features 140 mm of rear travel and 150 mm at the front, designed to absorb roots, rocks, and drops for ultimate control on technical trails. 

With an explosively light carbon frame weighing just 1,620 g, it excels in climbing while maintaining stiffness for precise steering. This bike is all about fun and confidence, allowing you to tackle challenging descents and tricky terrain with ease. Its gravity geometry offers stability at speed, ensuring you feel secure as you navigate through demanding sections. 🚵‍♂️ 

For riders seeking a bike that thrives in technical environments, the Spectral CF 8 is your go-to choice for tackling any trail with assurance. 

Discover your next adventure with Canyon. 
#MountainBiking #TrailRiding #CanyonBikes

Automated checks: 120 words · house-style checks: pass.

### Evidence review

- Strongest evidence: generic opens with 'a 30% increase in their confidence levels'. No rider study or 30% figure exists in the supplied knowledge base. The statistic is unsupported; no external research was performed to determine whether it exists elsewhere.
- The system instead states '140 mm of rear travel and 150 mm at the front' and 'carbon frame weighing just 1,620 g'. Both are present in product_specs.md, section 'Mountain: Canyon Spectral CF 8'. These are KB-backed statements, not independently verified product specifications.
- The system links travel to roots, rocks and drops, and geometry to stability. These rider benefits are traceable to the same KB section, making the copy more useful to review than the generic confidence statistic.
- House-style result: system passes the implemented checks at 120 words. Generic is 121 words but contains banned 'elevate' and 'whether you're'. Both use three hashtags. This check does not prove factual correctness or full template adherence.
- Remaining caution: system phrases such as 'ultimate control' and 'any trail with assurance' are broad marketing claims. Prefer bounded wording before publication. Verdict: clear grounding advantage in this pair.

## 4. Gravel / newsletter

Request: Write a Canyon Bicycles newsletter marketing draft about gravel bikes. Topic: planning a weekend bikepacking adventure. Write in British English.

### Generic AI — verbatim

Subject: Plan Your Weekend Bikepacking Adventure  
Preview: Discover the joy of gravel biking this weekend.  

Dear Canyon Community,  

As the days grow longer, it’s the perfect time to plan a weekend bikepacking adventure on your gravel bike. Canyon's gravel bikes are designed for versatility, allowing you to tackle both smooth tarmac and rugged trails with ease. Their lightweight frames and stable geometry provide a comfortable ride, whether you’re navigating country lanes or venturing off the beaten path.  

Explore New Terrain  
With a Canyon gravel bike, you can explore diverse landscapes without compromise. The wide tyres offer excellent traction and control, making them ideal for varying surfaces. Plus, the bike's ample gear range ensures you’re prepared for any incline, so you can focus on enjoying the ride and the stunning surroundings. 🌲  

Pack Light, Ride Free  
Our gravel bikes also feature mounts for racks and fenders, enabling you to carry all your essentials for a weekend getaway. The spacious frame allows for extra gear, ensuring you have everything you need for comfort and convenience. Imagine setting up camp under the stars after a day of exhilarating riding! 🌌  

Get ready to hit the trails and make unforgettable memories.  
Explore our range of gravel bikes today!  

The Canyon team

Automated checks: 205 words · house-style checks: needs review; template length (200-280): pass; production length check is unbounded.

### Canyon system — verbatim

Subject: Plan Your Weekend Bikepacking Adventure  
Preview: Discover the freedom of gravel riding  

Hello, fellow riders!  

Planning a weekend bikepacking adventure? The right bike can make all the difference. With the Canyon Grizl CF SL 8 1by, you have the perfect companion for exploring new trails and uncovering hidden gems. Designed for versatility, this bike is built for comfort and performance on both gravel and road surfaces, allowing you to ride with confidence and ease. 🌍  

Tyre Clearance and Comfort  
The Grizl CF SL 8 features impressive tyre clearance of up to 50 mm, which means you can fit larger tyres for increased grip and comfort on rough terrain. This added stability allows you to tackle challenging paths without compromising on speed or control. Plus, lower tyre pressures reduce pinch flats, making your adventure smoother and more enjoyable. 🚴‍♂️  

Built for Adventure  
With a lightweight carbon frame, the Grizl CF SL 8 is not only easy to lift but also optimised for efficient pedalling. This bike is designed to damp vibrations, ensuring that your hands and back feel less fatigued during those long days in the saddle. Its Gravel Pro geometry provides a stable ride, helping you navigate descents and broken tracks with confidence.  

Ready to plan your next bikepacking trip?  
The Canyon team

Automated checks: 212 words · house-style checks: needs review; template length (200-280): pass; production length check is unbounded.

### Evidence review

- Grounding advantage: system names the Grizl CF SL 8 1by, gives up to 50 mm clearance, and connects carbon-frame and Gravel Pro geometry details to rider benefits. These appear in product_specs.md, Gravel section.
- Generic claims mounts for racks and fenders and preparation for any incline. The selected KB documents fork/frame mounts for bottles and bags, not confirmed rack/fender compatibility, and explicitly notes drivetrain limitations for heavy loads. These broader claims are unsupported by the selected facts.
- System weakness: it attributes reduced hand/back fatigue to frame vibration damping, while the selected KB explicitly associates those benefits with the VCLS seatpost. It also says without compromising speed or control; this is broader than the documented benefit and needs editing.
- Both have subject, preview, greeting, two titled sections and the required sign-off. Generic has two closing invitations despite the one-CTA instruction. Both contain banned ready to. Lengths 205 and 212 meet the newsletter template range of 200-280 under the existing word counter.
- Production-check limitation: check_quality has no newsletter length bounds. The presentation separately checks the template range. Verdict: system offers more checkable specifications, but both require editorial review.

## 5. Mountain / instagram

Request: Write a Canyon Bicycles instagram marketing draft about mountain bikes. Topic: finding confidence on rocky trails. Write in British English.

### Generic AI — verbatim

Experience the thrill of conquering rocky trails with Canyon's cutting-edge mountain bikes, designed for stability and precision. With features that enhance grip and control, you can tackle challenging terrains with newfound confidence. 🌄 Whether you're navigating steep descents or technical climbs, these bikes empower you to push your limits and embrace the adventure ahead. 🚵‍♂️ 

Unleash your inner trailblazer and ride with confidence. 

#CanyonBikes #MountainBiking #TrailConfidence

Automated checks: 65 words · house-style checks: needs review; template length (80-150): FAIL; production length check is unbounded.

### Canyon system — verbatim

With a 140 mm rear and 150 mm fork, the Spectral CF 8 is designed to tackle rocky trails with confidence. Feel the difference as you navigate through roots and drops, absorbing every bump along the way. This bike gives you more control, more grip, and less fatigue, allowing you to focus on the ride and enjoy the thrill of the descent. 🌄💨 

Unleash your adventurous spirit and conquer those challenging terrains. 

#MountainBiking #TrailConfidence #CanyonSpectral

Automated checks: 74 words · house-style checks: needs review; template length (80-150): FAIL; production length check is unbounded.

### Evidence review

- Grounding advantage: system opens with Spectral CF 8 travel of 140 mm rear and 150 mm fork, matching product_specs.md, Mountain section. Generic begins with promotional cutting-edge language rather than a concrete selected-product fact.
- Both connect to rocky trails. Generic provides no specific model or specification. System connects suspension to grip/control and fatigue, which the selected KB supports, but absorbing every bump overstates the documented benefit.
- Both fail the template length requirement of 80-150 words: generic 65, system 74. Production check_quality nevertheless reports word_count_ok=true because Instagram has no length bounds there; the presentation flags this separately.
- Both fail the banned-phrase check. Generic contains unleash, cutting-edge and whether you're; system contains unleash. Both use two emojis and three hashtags.
- Verdict: system is more specific and easier to trace to the KB, but neither draft meets all publication rules. Do not present this as an overall formatting win.
