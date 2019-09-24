# Scraping Blizzard forums about World of Warcraft

Blizzard forums for their game World of Warcraft are a major source of information for the developers to get feedback from players. Numerous posts tackle the issues encountered by players in the game, and many posts contain insightful comments, and possible solutions to the problems encountered in the game.

##	Scraping Blizzard forum posts

For this task, we scraped the top posts over the past year on the [forums](https://us.forums.blizzard.com/en/wow/top). For each post, we collect the url, the title of the post and all of the comments in it. We removed any HTML items, and any quote (which appears when a user replies to another comment and quotes it). 

## Leveraging posts using natural language processing

The goal of this repository is to figure out whether we could create insights from those posts using natural language processing techniques.

## Latent-Dirichlet Allocation

The  idea is to see whether some topics could be related to people complaints, and automatically find out what words trigger complaints (thus finding out what are the controversial aspects of the game).

## Fine-tuning GPT-2 on this dataset

Just a fun experiment to see what GPT-2 can learn from this dataset. The notebook was taken from this [blogpost](https://minimaxir.com/2019/09/howto-gpt2/)




