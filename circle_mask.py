import numpy as np
from moviepy.editor import VideoFileClip, CompositeVideoClip

def make_circle_mask(clip):
    w,h = clip.size
    def mask_fn(get_frame,t):
        import numpy as np
        arr = get_frame(t)[:,:,0]  # shape h,w
        xx,yy = np.meshgrid(np.arange(w),np.arange(h))
        cx,cy = w/2, h/2
        r = min(w,h)/2
        mask = ((xx-cx)**2+(yy-cy)**2<=r**2).astype(float)
        return mask
    return clip.set_mask(clip.fl(mask_fn, apply_to=['mask']))

avatar = VideoFileClip('avatar.mp4', has_mask=True)
av = make_circle_mask(avatar)
# redimension et position plus tard