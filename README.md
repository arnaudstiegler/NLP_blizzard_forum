# Scraping Blizzard forums about World of Warcraft

Blizzard forums for their game World of Warcraft are a major source of information for the developers to get feedback from players. Numerous posts tackle the issues encountered by players in the game, and many posts contain insightful comments, and possible solutions to the problems encountered in the game.

##	Scraping Blizzard forum posts

To generate the data, we scraped the top posts over the past year on the [forums](https://us.forums.blizzard.com/en/wow/top). For each post, we collected the url, the title of the post and all of the comments in it. We removed any HTML items, and any quote (which appears when a user replies to another comment and quotes it). 

The data is available in the data folder (one file containing 1000 posts and one containing 10000 posts).

## Leveraging posts using natural language processing

The goal of this repository is to figure out whether we could create insights from those posts using natural language processing techniques.

## Sentiment Analysis on Forum Posts

Using Google Cloud Natural Language features, we did a sentiment analysis of the top-100 most actives posts: for each document (made of the inital post and all the answers), we extracted the sentiment score. We also extracted a sentiment score on the word level for each document, and aggregated the score to get an overall sentiment score for each word.

**The average sentiment score over the documents is -0.067** which indicates that the average sentiment is rather negative. However, the value is still very close to 0 which rather shows that there are mixed feelings among the posts. This score seems to correspond to the fact that although people do complain about the game, most of the posts aim at improving the game by providing feedback and are not only written to express dissatisfaction.

The top-10 most positive words are:
['fun','Classic','zones','example','class','power','games','life','ability','gear']
The top-10 most negative words are:
['problem','damage','issues','nothing','issue','People','Alliance','post',Blizzard','blizzard']
The results are interesting: "Classic" and 'classic' are among the top-10 most positive words within the posts which shows the enthusiasm of the players for the newly launched Classic WOW game. On the contrary, Blizzard has a very low score (you can actually find the occurence of Blizzard twice in the bottom 10 words).

Besides, it is interesting to note that 'zones', 'gear', 'class' have very high scores as well, which might indicte that those elements are the most-liked features of the game.

## Latent-Dirichlet Allocation

The  idea is to see whether some topics could be related to people complaints, and automatically find out what words trigger complaints (thus finding out what are the controversial aspects of the game).

## Fine-tuning GPT-2 on this dataset

Just a fun experiment to see what GPT-2 can learn from this dataset. The notebook was taken from this [blogpost](https://minimaxir.com/2019/09/howto-gpt2/). We used the 355M model of gpt-2 and trained it on all the comments we scraped (around 500k comments).

Here are some interesting samples from what the model can output once it has been trained on the Blizzard posts. They were generated using "I think the game" as prefix to "force" the model to talk about the game.

**Sample 1**

`<|startoftext|>I think the game is really kind of awful for PvE right now. Personally I’d play a monk, though I am currently leveling up hairlary as my main.I’ve stopped trying to do raid content. If Anduin continues on like this I see a lot more of this resource for connecting wpvp, don’t believe it or not.Server transfers, WQs, Warfronts, events/battlegrounds, etc are flaming and Blizz decided WoW’s covering? `

**Sample 2**

`<|startoftext|>I think the game suffers from being more myopic than usual.  On certain aspects I feel the game could use more work.  In particular, I want to take the opportunity to provide some feedback regarding the design of the on-focus mechanic.  Some parts of the gameplay rely on focused actions, I feel your light / purities thing would be more obtuse for the mechanic to work.I think at the current time the game adoption of focused actions is feeling musty and unbalanced.`

**Sample 3**

`<|startoftext|>I think the game does need to get imbalanced! I want new mobs, new dungeons, new skills, new PVE heroics, new storylines, new zones, new raids, new quests, as a lore point.Just as they should have placed guards on the fountain, placed idols all over the mythic dungeon, and gone skypie to see if they were equal? Reblasting the tomb 208 years ago does sound like an extra population.The idea that they’ve added the rotation of mechanic works like that when you do a one-time quest.`

We can see that the model has successfully captured some words that are specific to the game, and it uses them successfully: for instance "PVE" stands for player vs environment and is a very important component of the game. Similarly, it has captured some aspects of the games such as "mythic dungeons" or "raids". It has even learned that "monk" is a class of the game that you can play. The second interesting point is that the model has completely captured the general tone of the forum where people debate over aspects of the game and try to point out some of its weak points.

Of course, those examples were among the best: the model also ouputs a lot of unintelligible sentences. A bigger set of samples can be found in `gpt2_experiments/generation_samples/`. The notebook by Max Wolf that was used is located in the `/gpt2_experiments/` folder, but the weights cannot be uploaded because of the size of the file.

