# M6 — Generic AI vs Canyon

Prompt changes alone did not improve compliance.

In this single retest, system drafts meeting channel length fell from 3/5 to 1/5. Drafts with banned phrases stayed at 3/5. Product-specific grounding remains useful, but no overall improvement can be established from one stochastic sample per brief.

Reviewer: Codex review against the local KB; not independent or blind. Original outputs preserved separately.

## Method

Five fixed requests covering three product families and all four channels; ten generations, one per arm per request. All five pairs were freshly generated using the updated templates. Original results remain in the parent directory. The generic arm also received the updated format instructions, so this is not an isolated KB or single-rule experiment.
The generic baseline uses the same API model, language, format instructions and accuracy guidance,
without company documents. Our arm uses the real generate_draft pipeline with company context,
brand rules and banned-phrase guidance. This tests the whole product package, not the KB alone.
The customer here is the marketing user requesting content, not a support-ticket sender.
This is an API baseline, not a test of the ChatGPT application. Temperature is 0.7;
generation order alternates. All outputs are retained verbatim, including weaknesses.
Automated checks measure house style and length, not truth, persuasiveness or native-language quality.
One sample per case is illustrative, not statistical proof. No independent blind review was conducted.

Model: gpt-4o-mini; date UTC: 2026-10-23T13:29:52.297753+00:00; status: complete.

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

With a lightweight frame and versatile geometry, the Canyon Grizl is designed for an exhilarating ride across mixed terrain. As autumn paints the landscape, it's the perfect time to explore rugged trails and quiet country lanes, all while enjoying the vibrant colours of the season.

Gravel biking opens up a world of adventure, allowing you to tackle everything from smooth tarmac to bumpy dirt paths. Feel the crisp air as you navigate through fallen leaves, and experience the thrill of discovering hidden gems just off the beaten track. 🍂 Whether you're aiming for a weekend getaway or a leisurely ride with friends, the Grizl is your ultimate companion for autumn escapades. 

Get ready to embrace the freedom of gravel cycling – every ride is a new adventure waiting to unfold! 

#CanyonBikes #GravelCycling #AutumnAdventures

Automated checks: 131 words · house-style checks: needs review.

### Canyon system — verbatim

The Grizl CF SL 8 1by is designed for adventure, weighing just 9.5 kg (size M) and accommodating tyres up to 50 mm wide. This makes it an ideal companion for those autumn weekend rides on mixed terrain, where the crunch of gravel meets the thrill of exploration. 🍂 

With its stable geometry and lightweight carbon frame, the Grizl ensures that you can tackle descents and broken paths with confidence. Enjoy the freedom of venturing off the beaten track, discovering hidden trails and scenic routes, all while relishing the comfort of a bike that performs beautifully across diverse landscapes. 🌍

Are you ready to embrace the season and create unforgettable memories on your gravel bike? 

#GravelAdventure #CanyonBikes #ExploreMore

Automated checks: 117 words · house-style checks: needs review.

### Evidence review

- System uses documented Grizl 9.5 kg (size M) and up to 50 mm qualifiers correctly.
- Length regressed from 120 to 117 words; the 120-word minimum is missed. Banned ready to persists. The 160-word target was not followed.

## 2. Road / email

Request: Write a Canyon Bicycles email marketing draft about road bikes. Topic: comfortable long-distance rides for your next big day out. Write in British English.

### Generic AI — verbatim

Subject: Comfort for Your Long-Distance Rides  
Preview: Discover our road bikes for ultimate comfort.  

Dear cyclist,  

When planning your next big day out, comfort is key. Our road bikes are designed with long-distance rides in mind, ensuring you can tackle miles without discomfort. The ergonomic geometry and advanced frame materials provide a perfect balance of speed and stability, allowing you to enjoy the journey as much as the destination. 🚴‍♂️  

Whether you’re exploring scenic routes or taking on challenging terrains, our models feature meticulously crafted components that enhance your ride experience. The high-quality wheels and tyres offer excellent grip and durability, making every ride smooth and enjoyable. Plus, with options for customisation, you can tailor your bike to fit your unique riding style. 🌟  

Ready to elevate your cycling adventures?  
Explore our range today!  

The Canyon team

Automated checks: 138 words · house-style checks: needs review.

### Canyon system — verbatim

Subject: Comfort for Your Next Long Ride  
Preview: Ready for your next big day out?  

Hello,  

Long-distance rides should be enjoyable, not painful. With the Endurace, you can tackle those miles with confidence and comfort. Its "Sport" geometry offers a more relaxed riding position, reducing strain on your neck and back while providing stability on descents. 🚴‍♂️  

The VCLS seatpost enhances this comfort, absorbing vibrations to keep you feeling fresh, even after hours in the saddle. Plus, with a weight starting from just 7.52 kg, you’ll find climbing easier and more agile. 🌄  

Experience the perfect blend of speed and comfort on your next big adventure!  

Shop now to find your dream bike.  
The Canyon team

Automated checks: 116 words · house-style checks: needs review.

### Evidence review

- System associates comfort with Sport geometry and the VCLS seatpost, consistent with the Road KB. The weight claim preserves starting from 7.52 kg.
- Tyre-clearance qualifier handling is not tested because this draft omits clearance. Do not claim that the earlier by-version failure is resolved.
- Email remains short: 113 to 116 words, still below 120. Experience the perfect blend and Shop now form two closing promotional invitations despite the one-CTA rule.

## 3. Mountain / linkedin

Request: Write a Canyon Bicycles linkedin marketing draft about mountain bikes. Topic: confidence and control on technical trails. Write in British English.

### Generic AI — verbatim

Riders of the Canyon Spectral have reported a 20% increase in their confidence on technical trails. With precision engineering and cutting-edge geometry, our mountain bikes are designed to tackle the most challenging terrains, empowering you to conquer obstacles with ease.

The Spectral’s advanced suspension system delivers unparalleled control, allowing you to navigate rocky descents and steep climbs without hesitation. Experience the thrill of riding with complete stability, enabling you to focus on the trail ahead rather than worrying about your bike's performance. 🌄 Whether you're a seasoned pro or a budding enthusiast, our mountain bikes are built to elevate your ride and enhance your skills.

Join the community of riders who trust Canyon for their mountain biking adventures. Dare to push your limits and embrace the trails like never before. 

#CanyonBikes #MountainBiking #RideWithConfidence

Automated checks: 133 words · house-style checks: needs review.

### Canyon system — verbatim

The Spectral CF 8 is designed with 140 mm rear and 150 mm fork travel, providing the perfect blend of confidence and control on technical trails. This bike absorbs roots, rocks, and drops, ensuring you stay in command of your ride even on the toughest descents. 

With its gravity geometry and flip chip feature, you can easily tune the bike to suit your riding style, whether you prefer agile cornering or stable descents. The playful character of the Spectral CF 8 makes every ride an adventure, allowing you to tackle varying terrain with ease and have fun while doing it. 🌲💨 

Experience the thrill of exploration and discover the trails like never before. 

#MountainBiking #TrailRiding #CanyonBikes

Automated checks: 115 words · house-style checks: needs review.

### Evidence review

- The system retains documented Spectral suspension figures and connects flip chip/geometry to tunability.
- Length regressed from 120 to 115 words. No banned phrases appear, but no all-checks pass is achieved. Absolute language about even the toughest descents remains worth editing.

## 4. Gravel / newsletter

Request: Write a Canyon Bicycles newsletter marketing draft about gravel bikes. Topic: planning a weekend bikepacking adventure. Write in British English.

### Generic AI — verbatim

Subject: Plan Your Weekend Bikepacking Adventure  
Preview: Discover the perfect gravel bike for you.  

Dear Canyon Enthusiast,  

As the weekend approaches, it's the perfect time to plan your next bikepacking adventure. With our range of gravel bikes, you can explore uncharted paths and enjoy the thrill of off-road cycling. Our gravel bikes are designed to provide comfort and stability on a variety of terrains, making them ideal companions for weekend getaways.  

Ride with Confidence  
Our gravel bikes, like the Grail, feature a lightweight frame and wide tyres that allow for a smooth ride over rough trails. The geometry is tailored for long-distance comfort, ensuring you can tackle those challenging routes without fatigue. Plus, with ample gear options, you can carry everything you need for a weekend escape. 🌄  

Pack Smart  
When gearing up for your adventure, remember that our gravel bikes offer integrated storage solutions. From frame bags to handlebar packs, you can easily organise your essentials without sacrificing performance. This thoughtful design allows you to carry tools, snacks, and a sleeping bag, ensuring you’re well-prepared for a night under the stars. 🌌  

Explore the great outdoors with our exceptional gravel bikes and make this weekend one to remember!  

Happy riding!  
The Canyon team

Automated checks: 205 words · house-style checks: pass; template length (200-280): pass; production length check is unbounded.

### Canyon system — verbatim

Subject: Plan Your Weekend Bikepacking Adventure  
Preview: Discover the joy of gravel riding  

Hello Gravel Riders,  

As the weekend approaches, it's the perfect time to plan your next bikepacking adventure. With the right gear, you can explore new trails and enjoy the freedom that gravel riding offers. The Canyon Grizl CF SL 8 1by is designed to take you wherever your spirit of adventure leads, making it an ideal companion for your journey.  

Tyre clearance is essential for a bikepacking trip, and the Grizl accommodates up to 50 mm tyres. This feature provides more grip and comfort on gravel and loose dirt, allowing you to navigate diverse terrains confidently. You can lower your tyre pressures for enhanced comfort and fewer pinch flats, ensuring a smoother ride on long days. 🚴‍♂️  

Packing for your adventure is made easier with the Grizl's frame mounts, perfect for securing bottles and bags. You can carry everything you need for multi-day trips, from spare clothing to camping gear, making your bike truly versatile. With the Grizl, you can enjoy the freedom to pack light and ride far, ready for any adventure that awaits. 🏞️  

Get ready to hit the trails!  

Explore the Canyon Grizl today.  

The Canyon team

Automated checks: 202 words · house-style checks: needs review; template length (200-280): pass; production length check is unbounded.

### Evidence review

- System uses up to 50 mm and frame mounts for bottles/bags from the Gravel KB. The prior frame/seatpost fatigue conflation does not recur, but that feature was omitted, so this does not prove the causal rule is reliably followed.
- Newsletter is 202 words, within 200-280 but below the 240-word target. It omits the required two section titles and ends with two invitations. Banned journey and ready to appear.
- Production length checking remains unbounded for newsletters; the separate report check supplies the real range.

## 5. Mountain / instagram

Request: Write a Canyon Bicycles instagram marketing draft about mountain bikes. Topic: finding confidence on rocky trails. Write in British English.

### Generic AI — verbatim

Our mountain bikes are engineered with cutting-edge suspension systems for unmatched stability on rocky terrain. 

Conquer the most challenging trails with confidence! 🏞️ Feel the adrenaline rush as you navigate through rocky paths, knowing your bike is designed to absorb every bump and jolt. With superior grip and control, you can focus on the thrill of the ride while pushing your limits. 🚵‍♂️ Embrace the rugged beauty of nature, and let each ride empower you to tackle new adventures.

Join us and elevate your mountain biking experience today!  
#MountainBiking #TrailConfidence #CanyonBikes

Automated checks: 90 words · house-style checks: needs review; template length (80-150): pass; production length check is unbounded.

### Canyon system — verbatim

With 140 mm rear and 150 mm front suspension, the Spectral CF 8 is designed to absorb roots, rocks, and drops, giving you more control on rugged trails. 🌄 Feel the confidence grow as you tackle challenging terrain, knowing your bike is built to handle the toughest obstacles. The playful character of the Spectral makes every ride a chance to push your limits and discover new paths.

Ready to take on the trails? 

#CanyonBikes #MountainBiking #RideWithConfidence

Automated checks: 75 words · house-style checks: needs review; template length (80-150): FAIL; production length check is unbounded.

### Evidence review

- System gives documented 140 mm rear/150 mm front suspension. Broad toughest obstacles language still needs review.
- Instagram grows from 74 to 75 words but still fails the 80-word minimum and contains ready to. Production word_count_ok=true is misleading because this channel is unbounded in check_quality.
