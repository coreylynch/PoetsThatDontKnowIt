Description
===========

This bot builds haikus algorithmically from the twitter public timeline and then publishes them back to twitter. It uses online LDA (http://www.cs.princeton.edu/~blei/papers/HoffmanBleiBach2010b.pdf) to assign a topic to each incoming tweet. If it can find two other tweets with the same topic and compatible syllabic structure (i.e. 5-7-5), it concatenates them into a haiku and pushes the haiku to the twitter handle over tweepy. If it can't find suitable matches, the tweet is stored in mongodb alongside its assigned topic (and hashtag if available), and the process continues.

Examples
========

\#dancing : "the storm is coming // my eyes are closing slowly // dancing in the dark" -- @miss_kocix, @_NoPhotoShop_, @samanthastari

\#paper : "stop the tape rewind // absolutely love this song // never heard this song" -- @VAS__HAPPINEN, @All1DRush, @angela1014

\#never : "now it all make sense // laughing like never before // lifes what you make it" -- @Sincerew, @Susysaurus, @Hierooglyphics

\#valentines : "happy valentines // worst valentines day ever // fuck valentines day" -- @slokita, @Arau_u, @jLOUDpack

\#ate : "i just learned something // i see the blood in your eyes // im sorry good bye" -- @A_Renee__, @anaaak, @AndiNovaL_

\#program : "did i spell stress rite // messing up the breathing air // in the air i breath" -- @checkz_NP, @QuietKid214, @Ennaooh

\#struggle : "so adorable // this audience is brutal // the struggle is real" -- @maythangnam, @According2Esha, @SophisticatedA_

\#people : "good morning people // people are so ungrateful // why is the rum gone" -- @sherlylolytia, @phokingdom, @PresDareing

\#food : "i have so much rage // my damn hand in soo much pain // i love grapes so much" -- @hollymbolly, @RayNasty_Laydee,

\#hate : "bout to take this nap // im ready to take the black // its dark already" -- @FreshR_Than_HIM, @viserys4king, @thats_just_PAUL

\#hate : "feeling terrible // i wish i could have quit you // i hate you really" -- @Dilara889, @Dr0pDeadCunt, @nadiviajovanka

\#friends : "forever alone // so to all my followers // why cant we be friends" -- @_BeliebersDoJus, @C_LAYSitdown, @sl_hutchins

\#ignorant : "big booty judy // just made some bomb ass breakfast // diamonds in her veins" -- @Amari_Byrd, @ABitchPipeDown, @nathirobinzon

See more at https://twitter.com/#!/favorites 

Some words from the authors
===========================
* "A surreal bot" - @xmclearyx
* "lol smooth poem i guess" - @Ordinary_nahh
* "thats a quote from robin hood you idiot and who the fuck are you to judge my philisophical standards ?" - @novahmilaar
* "Wat does dat even mean?? Dude u high" - @Omarvelli
* "if I don't know you don't fuckin talk to me. #square" - @TrillOG_B

Dependencies
============
* Tweetstream
* NLTK
* Tweepy