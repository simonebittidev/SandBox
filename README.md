# SandBox

This experimental project explores the potential of AI as an autonomous decision-maker for a virtual world. Using Azure OpenAI and a structured prompt-response loop, the system generates daily high-level decisions on critical areas such as economy, society, environment, and global politics. Each decision is designed to be realistic, impactful, and ethically informed, balancing immediate outcomes with long-term sustainability. The goal is to create an engaging and evolving narrative that demonstrates the capabilities of generative AI while inviting users to reflect on governance and the complexities of decision-making in a simulated world. [Read more](https://abozar-alizadeh.medium.com/exploring-ai-driven-governance-building-a-virtual-world-where-ai-rules-22419690a409)

I invite you to explore the very simple interface at https://genbox.azurewebsites.net/, where you can witness the AI’s daily decisions and follow the evolving narrative of this virtual world.

![TV](https://github.com/abozaralizadeh/SandBox/blob/main/static/sample.png?raw=true)

gunicorn --bind=0.0.0.0 --timeout 600 main:app
