
# Inspiration

As an avid road trip enthusiast, I always felt like I was missing out on great experiences for simply not knowing about them. Having a tool that allows me to find the best places and routes them in the palm of my hand makes road-tripping an easier time than ever.

# What it does

WonderWays can find "Wonders" along the trip when given a starting and ending location. Support points of interest include outlets, restaurants, museums, hiking trails, or hotels, which the user can select up to 2 for WonderWays to search along the starting and ending locations. The users then can select up to 9 "Wonders" to add between their starting and ending location and will generate a Google Map plan for their WonderWays road trip.

# How we built it

Venkat and I built this entire project in Python. At the heart of this project lies ChatGPT-4, or BingChat, which powers the search of "Wonders" between two given locations. We develop a custom prompt that communicates with the AI model to construct a viable itinerary with the user's interest in mind.

# Challenges we ran into

The biggest challenge we faced while doing this project was developing a prompt that could make the chatbot generate responses in a reliable and predictable way so that we could parse the response. The reason for this is that BingChat, unlike OpenAI's ChatGPT, is connected to the internet, allowing for more up-to-date information, which is vital for anyone roading trips.

# Accomplishments that we're proud of

One accomplishment we are incredibly proud of was converting the command-line interface we originally planned into a UI that users can easily interact with. This was our first time attending a hackathon, and we initially thought that developing a UI would be an impossible challenge for us, but we managed to pull through.

# What we learned

We did not give up when faced with the pseudo-random output nature of what BingChat could generate. Through our perseverance, we learned how to properly prompt the chatbot to get responses that were predictable nearly all of the time; furthermore, we honed our skills at parsing strings from all of the wrong responses BingChat would give to us before we found out how to prompt it properly.

# What's next for WonderWays

We plan to decrease the chatbot's inference time to respond to our prompt. We think that having BingChat generate the entire response at once is slowing it down, and streaming the answer one character at a time would increase its speed. We also plan to overhaul the basic UI with a more complex but equally visually appealing interface that speaks to our design standards.

# Watch our project in action!

🚀[Video Demo](https://www.youtube.com/watch?v=RCOXR41Ml_k)


![Image](https://github.com/VenkatKandhipati/wonderways/blob/eb5ca44a30cd578848f6f43155d673cfcf2d85e9/image.png)
