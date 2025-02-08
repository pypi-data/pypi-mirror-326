import tensorflow as tf
from moviepy.video.fx import AccelDecel
from moviepy.video.VideoClip import DataVideoClip


class ImageToVideoConverter:
    def __init__(self, max_frames_to_sample):
        self.frames_for_vid: list = []
        self.max_frames_to_sample: int = max_frames_to_sample
        self.curr_frame_idx: int = 0

    def to_video(output_path, duration, fps=60):
        self.upsample()

        print(f"Number of images to frame: {len(self.frames_for_vid)}")

        vid = DataVideoClip(self.frames_for_vid, lambda x: x, fps=fps)
        vid = AccelDecel(new_duration=duration).apply(vid)
        vid.write_videofile(output_path)

    def upsample():
        NUM_FRAMES_TO_INSERT = 60

        new_frames = []

        # Upsample via frame-frame interpolation
        for i in range(len(self.frames_for_vid) - 1):
            frame1 = tf.cast(self.frames_for_vid[i], tf.float32)
            frame2 = tf.cast(self.frames_for_vid[i + 1], tf.float32)

            new_frames.append(self.frames_for_vid[i].numpy())  # Add original frame

            interpolated = interpolate_frames(frame1, frame2, NUM_FRAMES_TO_INSERT)
            new_frames.extend(interpolated.numpy())

        new_frames.extend(
            [self.frames_for_vid[-1].numpy()] * 60 * 3
        )  # Lengthen end frame by 3 seconds
        self.frames_for_vid = new_frames

    @tf.function
    def interpolate_frames(frame1, frame2, num_frames):
        alphas = tf.linspace(0.0, 1.0, num_frames + 2)[1:-1]  # Avoid 0 and 1

        frame1 = tf.cast(frame1, tf.float32)
        frame2 = tf.cast(frame2, tf.float32)

        interpolated_frames = (1 - alphas[:, None, None, None]) * frame1 + alphas[
            :, None, None, None
        ] * frame2
        return tf.cast(interpolated_frames, tf.uint8)
