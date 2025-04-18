from moviepy.editor import VideoFileClip, CompositeVideoClip
# slides + audio
slides = VideoFileClip('slides_video.mp4')
av = VideoFileClip('avatar.mp4', has_mask=True).subclip(0,slides.duration)
# circle mask application si besoin
w,h = slides.size
av = av.resize(width=w*0.2).set_position(('right','bottom'))
final = CompositeVideoClip([slides, av])
final.write_videofile('video_finale.mp4', fps=24)