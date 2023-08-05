====================
Products.JWPlayer
====================

To use this extension, you must have done the following:
    * Rightly set up your plone site and configure it to use the TinyMCE editor for content editing.
    * Created a JWPlayer account at https://jwplayer.com.
    * Familiarize yourself with the basic configuration of the jwplayer. See `configuration options here <https://developer.jwplayer.com/jw-player/docs/developer-guide/customization/configuration-reference/#setup>`_



Inserting Video Content via TinyMCE
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


When Products.JWPlayer extension is installed, a toolbar button is added to the TinyMCE editor called "Insert/Edit JWPlayer Element".
A click on this button pops up the configuration dialog for the player. Below we explain the various configuration options:
    
1. Hosting Type
---------------

With jwplayer, one could choose either to self-host the entire library or use a cloud based player on the jwplayer platform (https://jwplayer.com)
The first step of the configuration is to select if your player will be self-hosted or cloud hosted

2. Self-hosted Player
---------------------

Settings:
    * *Player Library URL* : Specify the URL to the jwplayey library javascript file. Example: http://example.com/jwplayer/jwplayer.js
    * *JWPlayer Key*: When you decide to download the jwplayer library to host yourself, a key is provided to you which is required for the self-hosted player to work. You need to input that key in this field.

3. Cloud based Player
---------------------

Setting:
    * *Player Library URL* : Specify the URL to your cloud based player JavaScript library. You can see this URL when you sign-in to the jwplayer platform and check you list of created players.
    
4. Video Source
----------------

Setting:
    * *Video URL* : Enter the absolute URL of the video which you want to be played. You could enter multiple sources to the same video by using a double pipe (**||**), also known as the logical _OR_ operator.
    
5. Player Settings
------------------

Setting:
    * *Player Settings* : You could configure the player that will be embedded using this field. jwplayer comes with a number of configuration options when setting up the player.

    Each setting should be entered **in a new line**. For this field, only simple key-value pair settings are supported and each setting should be entered in the form **key = value**. A list of configurable jwplayer options can be seen `here <https://developer.jwplayer.com/jw-player/docs/developer-guide/customization/configuration-reference/#setup>`_
    

Once you are done configuring the options in the dialog, you can use the "Preview" button to have glimpse of your video.
Click on "Insert", in order to insert the video content into the TinyMCE editor. Save your plone object and view. Your video should rightly play if all was configured correctly.
