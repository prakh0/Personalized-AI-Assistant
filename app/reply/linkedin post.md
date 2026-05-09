I’ve been continuing work on my personal AI agent that can execute tasks autonomously on my behalf.

Initially, it was just replying to messages using a local Qwen 4B model running on my MacBook. But over the past few iterations, I’ve been focusing to make it more personalized.

Here’s what’s new:

•⁠  Added personalized memory so the agent can adapt its responses based on user preferences and past interactions.
•⁠  ⁠It can reply to messages on gmail and WhatsApp. It can search for files with relevant information and send them as attachements.
•⁠  ⁠I’ve reworked the architecture so both platforms share the same logic and memory layer.
•⁠  Now it can also switch between different models.
•  Users can subscribe to various apps offered by the agent to execute specific tasks. For example, I have a market research app that sends me daily summaries of the stock market.

The flow is still similar at a high level:

•⁠  ⁠WhatsApp: Incoming message → ngrok → local backend → LLM → reply sent
•⁠  ⁠Gmail: Incoming email → Gmail API → local backend → LLM → reply sent

Running lightweight models locally still works great (even tested smaller models like qwen 2b on a Raspberry Pi 5 with 8GB RAM), but having flexibility with different models opens up a lot more possibilities.

The goal is to enjoy the process of building and learning, while creating something that’s genuinely useful in my daily life.

I will put the source code on GitHub soon for anyone interested in exploring.