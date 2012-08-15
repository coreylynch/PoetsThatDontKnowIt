Description
===========

This bot builds haikus on the fly from a sample of the twitter public timeline. It uses Blei's implementation of online LDA to assign tweets one of 200 topics (which vary over time). If it can find two other tweets with the same topic and compatible syllabic structure (i.e. 5-7-5), it concatenates them into a haiku and pushes the haiku to the twitter handle over tweepy. If it can't find suitable matches, the tweet is stored in mongodb alongside its assigned topic (and hashtag if available), and the process continues.

Examples
========

\#dancing : "the storm is coming // my eyes are closing slowly // dancing in the dark" -- @miss_kocix, @_NoPhotoShop_, @samanthastari

paper : "stop the tape rewind // absolutely love this song // never heard this song" -- @VAS__HAPPINEN, @All1DRush, @angela1014

valentines : "happy valentines // worst valentines day ever // fuck valentines day" -- @slokita, @Arau_u, @jLOUDpack

shots : "might be up all night // sometimes i get jealous to // i cant handle this" -- @_Jshine, @Berry_Says, @Squeeb_Slayer

ate : "i just learned something // i see the blood in your eyes // im sorry good bye" -- @A_Renee__, @anaaak, @AndiNovaL_

people : "good morning people // people are so ungrateful // why is the rum gone" -- @sherlylolytia, @phokingdom, @PresDareing

handbook : "bout to cook breakfast // really wish i was sleeping // my moms very sick" -- @youLOST_Jai, @DiamondXCIV,

friends : "forever alone // so to all my followers // why cant we be friends" -- @_BeliebersDoJus, @C_LAYSitdown, @sl_hutchins

ignorant : "big booty judy // just made some bomb ass breakfast // diamonds in her veins" -- @Amari_Byrd, @ABitchPipeDown, @nathirobinzon

See more at https://twitter.com/#!/favorites 

Dependencies
============
* Tweetstream
* NLTK
* Tweepy