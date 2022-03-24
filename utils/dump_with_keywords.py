import pandas as pd
import pathlib
import os
from tqdm import tqdm
import argparse


def dump_wiki(TOPIC_DIR, RESULT_DIR):
    df = pd.read_csv(TOPIC_DIR)
    topics = dict()
    for _, data in df.iterrows():
        topics[data["topic"]] = [k.strip() for k in data["keywords"].split(",")]

    for key in tqdm(topics.keys()):
        print(f"Topic: {key}")
        if not os.path.exists(os.path.join(RESULT_DIR, key)):
            os.makedirs(os.path.join(RESULT_DIR, key))
        for keyword in tqdm(topics[key]):
            print(f"Keyword: {keyword}")
            os.system(
                f'wikiextract sentence extract --name "{keyword}" --data-dir /home/nas/wiki_dump/contents/ --idxbook idxbook.tsv --save-dir {RESULT_DIR}/{key}/ --kss --line-length 15'
            )
    print("Done!")
    return


def count_sents(RESULT_DIR, OUTPUT_DIR):
    path = pathlib.Path(RESULT_DIR)
    files = list(path.glob("**/*.txt"))

    current_topic = str(files[0]).split("/")[-2]
    line_total = 0
    with open(OUTPUT_DIR, "w") as fw:
        fw.write
        for file in tqdm(files):
            if current_topic != str(file).split("/")[-2]:
                fw.write(f"Total sentence length : {line_total}\n\n")
                current_topic = str(file).split("/")[-2]
                line_total = 0

            lines = open(file).readlines()
            fw.write(f"{str(file).replace(RESULT_DIR, '')}: {len(lines)}\n")
            line_total += len(lines)
        fw.write(f"Total sentence length : {line_total}\n\n")
    print(f"Number of documents saved in {OUTPUT_DIR}")
    return


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--topic_dir", type=str, required=True, help="topics & keywords file"
    )
    parser.add_argument(
        "--result_dir", type=str, default="results/", help="result file"
    )
    parser.add_argument(
        "--output_dir", type=str, default="num_sents.txt", help="result file"
    )
    args = parser.parse_args()
    dump_wiki(args.topic_dir, args.result_dir)
    count_sents(args.result_dir, args.output_dir)
