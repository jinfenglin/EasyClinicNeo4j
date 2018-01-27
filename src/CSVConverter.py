import csv, os
from common import *


def clean_artifact_name(artifact_name):
    artifact_name = artifact_name.split('-')[1].strip("\n\t ")
    artifact_name = " ".join([x for x in artifact_name.split(' ') if (len(x) > 0)])
    artifact_name = artifact_name.replace(' ', '_').lower()
    return artifact_name + '.csv'


def get_writing_path(source_root_path):
    """
    Generate the path where the csv files should write to
    :param source_root_path: The root directory of a certain package like 'docs-10.0%'
    :return:
    """
    package_name = os.path.basename(source_root_path)
    return os.path.join(CSV_DIR, package_name)


def artifact_convert(doc_dir_path):
    """
    Covnvert the artifact into csv format, each artifact is represented with id and content
    :param doc_dir_path: The directory root of the artifacts
    :return:
    """
    for dir_name in os.listdir(doc_dir_path):
        artifact_dir_path = os.path.join(doc_dir_path, dir_name);
        csv_file_name = clean_artifact_name(dir_name)
        csv_pack_dir_path = get_writing_path(doc_dir_path)
        if not os.path.isdir(csv_pack_dir_path):
            os.makedirs(csv_pack_dir_path)
        with open(os.path.join(csv_pack_dir_path, csv_file_name), 'w', newline='', encoding='utf8') as fout:
            writer = csv.writer(fout, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
            writer.writerow(['id', 'content'])
            for file_name in os.listdir(artifact_dir_path):
                file_path = os.path.join(artifact_dir_path, file_name)
                with open(file_path, encoding='utf8') as fin:
                    content = fin.read().replace('\n', ' ')
                    id = file_name.replace(".txt", "")
                    writer.writerow([id, content])


def relation_convert(doc_dir_path):
    relation_dir = os.path.join(DATA_DIR, 'relations')
    csv_pack_dir_path = get_writing_path(doc_dir_path)
    if not os.path.isdir(csv_pack_dir_path):
        os.makedirs(csv_pack_dir_path)
    for file_name in os.listdir(relation_dir):
        file_path = os.path.join(relation_dir, file_name)
        relation_csv = os.path.join(csv_pack_dir_path, file_name.replace(".txt", ".csv"))
        with open(file_path) as fin, open(relation_csv, 'w', newline='') as fout:
            csv_writer = csv.writer(fout, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
            csv_writer.writerow(['from', 'to'])
            for line in fin.readlines():
                parts = line.split(":")
                fromArtif = parts[0].strip("\n\t\r ").replace('.txt', '')
                toArtifs = [x.strip("\n\t\r ") for x in parts[1].split(" ")]
                toArtifs = [x for x in toArtifs if len(x) > 0]
                for toArtif in toArtifs:
                    toArtif = toArtif.replace(".txt", '')
                    csv_writer.writerow([fromArtif, toArtif])


if __name__ == '__main__':
    artifact_convert(os.path.join(DATA_DIR, "2 - docs (English)"))
    relation_convert(os.path.join(DATA_DIR, "2 - docs (English)"))
    percent = 0.0
    for i in range(0, 10):
        percent += 0.1
        package_name = "docs-{}%".format(round(percent * 100, 2))
        artifact_convert(os.path.join(DATA_DIR, package_name))
        relation_convert(os.path.join(DATA_DIR, package_name))
