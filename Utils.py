import os.path

dataset_path = '../datasets/iam_words/words.txt'

def get_img_path_and_text(partition_split_file):
    paths_and_texts = []

    with open(partition_split_file) as f:
        partition_folder = f.readlines()
    partition_folder = [x.strip() for x in partition_folder]

    with open(dataset_path) as f:
        for line in f:
            if not line or line.startswith('#'):    # skip empty line or line start with #
                continue
            line_split = line.strip().split(' ')
            assert len(line_split) >= 9
            segmentation_status = line_split[1]
            if segmentation_status == 'er':         # skip line with segmentation status 'er' : segmentation of word can be bad
                continue

            # image file
            split_file_name = line_split[0].split('-')
            img_dir = split_file_name[0]
            img_sub_dir = '{}-{}'.format(split_file_name[0], split_file_name[1])
            img_name = '{}.png'.format(line_split[0])
            img_path = os.path.join('../datasets/iam_words/words', img_dir, img_sub_dir, img_name)

            gt_text = ' '.join(line_split[8:])      # extract ground truth and skip longer than 16 chars
            if len(gt_text) > 16:
                continue
            if img_sub_dir in partition_folder:
                paths_and_texts.append([img_path, gt_text])     # append image path and transcript in list

            print(paths_and_texts)

get_img_path_and_text('../datasets/iam_words/words')