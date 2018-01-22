import csv, os

DATA_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'data')
EASY_CLINIC_ENG = os.path.join(DATA_DIR, '2 - docs (English)')
CSV_DIR = os.path.join(DATA_DIR, 'csv')


def clean_artifact_name(artifact_name):
    artifact_name = artifact_name.split('-')[1].strip("\n\t ")
    artifact_name = " ".join([x for x in artifact_name.split(' ') if (len(x) > 0)])
    artifact_name = artifact_name.replace(' ', '_').lower()
    return artifact_name + '.csv'


def artifact_convert():
    for dir_name in os.listdir(EASY_CLINIC_ENG):
        artifact_dir_path = os.path.join(EASY_CLINIC_ENG, dir_name);
        csv_file_name = clean_artifact_name(dir_name)

        with open(os.path.join(CSV_DIR, csv_file_name), 'w', newline='') as fout:
            writer = csv.writer(fout, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
            writer.writerow(['id', 'content'])
            for file_name in os.listdir(artifact_dir_path):
                file_path = os.path.join(artifact_dir_path, file_name)
                with open(file_path) as fin:
                    content = fin.read().replace('\n', ' ')
                    id = file_name.replace(".txt", "")
                    writer.writerow([id, content])


def relation_convert():
    relation_csv = os.path.join(CSV_DIR, 'relation.csv')
    relation_dir = os.path.join(DATA_DIR, 'relations')
    with open(relation_csv, 'w', newline='') as fout:
        csv_writer = csv.writer(fout, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
        csv_writer.writerow(['from', 'to'])
        for file_name in os.listdir(relation_dir):
            file_path = os.path.join(relation_dir, file_name)
            with open(file_path) as fin:
                for line in fin.readlines():
                    parts = line.split(":")
                    fromArtif = parts[0].strip("\n\t\r ").replace('.txt', '')
                    toArtifs = [x.strip("\n\t\r ") for x in parts[1].split(" ")]
                    toArtifs = [x for x in toArtifs if len(x) > 0]
                    for toArtif in toArtifs:
                        toArtif = toArtif.replace(".txt", '')
                        csv_writer.writerow([fromArtif, toArtif])


if __name__ == '__main__':
    artifact_convert()
    relation_convert()
