import os
import datetime as dt
import upload
import copy

def stitch_and_compress(video_path, today):
    for root_, dir_, file_ in os.walk(video_path):
        s = ''
        # WRITE THE INPUT FILES
        for file in file_:
            if file.endswith('.MP4'):
                s += 'file \'{}\'\n'.format(os.path.join(root_, file))
        if s:
            with open(os.path.join(root_,'input.txt'), 'w') as f:
                f.write(s)
        # STITCH THE VIDEO AND COMPRESS
        print('Stitching file {}_{}\n'.format(os.path.join(root_, os.path.split(root_)[-1]), today))
        os.system('ffmpeg -hide_banner -loglevel error -f concat -safe 0 -i {} -codec copy {}_{}_long.mp4'.format(os.path.join(root_,'input.txt'), os.path.join(root_, os.path.split(root_)[-1]), today))
        
        print('Compressing file {}_{}\n'.format(os.path.join(root_, os.path.split(root_)[-1]), today))
        os.system('ffmpeg -hide_banner -loglevel error -i {}_{}_long.mp4 -vcodec libx265 -crf 14 {}_{}.mp4'.format(os.path.join(root_, os.path.split(root_)[-1]), today, os.path.join(root_, os.path.split(root_)[-1]), today))
    
def remove_old_videos(video_path, today):
    for root_, dir_, file_ in os.walk(video_path):
        for f in file_:
            if f.strip('.mp4') != '{}_{}'.format(os.path.split(root_)[-1], today):
                try:
                    os.remove(os.path.join(root_, f))
                except FileNotFoundError:
                    pass

def upload_to_youtube(video_path, arg_dict, today):
    for root_, dir_, file_ in os.walk(video_path):
        for f in file_:
            if f.lower().endswith('.mp4'):
                completed_arg_dict = copy.deepcopy(arg_dict)
                completed_arg_dict['file'] = os.path.join(root_, f)
                completed_arg_dict['title'] = '{}'.format(f.strip('.mp4'))
                completed_arg_dict['description'] = '{}'.format(f.strip('.mp4'))
                upload.main(completed_arg_dict)

def main(video_path, arg_dict, today):
    stitch_and_compress(video_path, today)
    remove_old_videos(video_path, today)
    upload_to_youtube(video_path, arg_dict, today)


if __name__ == '__main__':
    desktop = os.path.abspath(os.path.join(os.environ['HOMEPATH'], 'Desktop'))
    ffmpeg_path = os.path.join(desktop, 'ffmpeg', 'bin')
    video_path = os.path.join(desktop, 'Vidstitch')
    today = dt.datetime.strftime(dt.datetime.now(), '%b_%d_%Y')

    arg_dict = {'auth_host_name': 'localhost', 
                'noauth_local_webserver': False, 
                'auth_host_port': [8080, 8090], 
                'logging_level': 'ERROR', 
                'file': None, 
                'title': '', 
                'description': '', 
                'category': '22', 
                'keywords': 'Volleyball, Hermosa, Beach, TOPSECRETTRAININGFOOTAGE', 
                'privacyStatus': 'unlisted'}
    
    main(video_path, arg_dict, today)