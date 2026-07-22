function lapse --wraps='ffmpeg -i input.mp4 -vf "fps=10,setpts=0.016*PTS" -an output.mp4' --description 'alias lapse ffmpeg -i input.mp4 -vf "fps=10,setpts=0.016*PTS" -an output.mp4'
    ffmpeg -i $argv -vf "fps=10,setpts=0.016*PTS" -an output.mp4
end
