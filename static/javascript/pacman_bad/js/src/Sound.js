define([
'jquery', 
'SoundWrapper', 
'SoundPool', 
'gameQuery'
], function($, SoundWrapper, SoundPool) {
    var Sound = {
        active : true,

        init : function(active) {
            this.active = active;
            if (!this.active) return;

            this.sounds = {
                intro : new SoundWrapper('static/javscript/pacman/audio/intro.mp3'),
                back : new SoundPool('static/javscript/pacman/audio/audio/back.mp3', 20),
                dot : new SoundPool('static/javscript/pacman/audio/audio/dot.mp3', 20),
                eaten : new SoundWrapper('static/javscript/pacman/audio/audio/eaten.mp3'),
                eat : new SoundPool('static/javscript/audio/pacman/audio/eat.mp3', 8),
                frightened : new SoundWrapper('static/javscript/pacman/audio/audio/frightened.mp3'),
                dead : new SoundPool('static/javscript/pacman/audio/audio/dead.mp3', 20),
                bonus : new SoundWrapper('static/javscript/pacman/audio/audio/bonus.mp3'),
                life : new SoundWrapper('static/javscript/pacman/audio/audio/life.mp3')
            };
        },
        
        play : function(label) {
            if (!this.active) return;
            this.sounds[label].play();
        },

        muted : function(muted) {
            $.muteSound(muted);
        }

    };

    return Sound;

});
