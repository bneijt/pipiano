Installation
============

    git clone this repo /opt/pipiano
    sudo /opt/pipiano/install.sh

Configure connection

    aconnect -l

    aconnect 128

    sudo fluidsynth --gain 1.5 --server --audio-driver=alsa /usr/share/sounds/sf2/FluidR3_G*


Configure velocity to minimum

    router_clear
    router_begin note
    router_par2 0 39 0 40
    router_end
    router_begin note
    router_par2 40 100 1 0
    router_end
    router_begin note
    router_par2 101 127 0 100
    router_end


    router_clear
    router_begin note
    router_par2 0 100 0 100
    router_end
    router_begin note
    router_par2 101 127 0 100
    router_end


