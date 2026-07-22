function txcp --wraps='g++' --description 'compile random source files'
    # parse
    set -l bool_doRun 0
    set -l args
	set -l runArgs

    for i in $argv
		if test "$bool_doRun" = "0"
			if test "$i" = "-r"
    	        set bool_doRun 1
    	    else
    	        set -a args $i
    	    end
		else
			set -a runArgs $i
		end
    end

    # echo "$bool_doRun"
    # echo "$args"
    # run
    g++ $args -o ~/AppData/CompiledFiles/bin -std=c++20
	echo "Compile Finished; Binary path: ~/AppData/CompiledFiles/bin"
    if test $bool_doRun = 1
        ~/AppData/CompiledFiles/bin $runArgs
    end
end
