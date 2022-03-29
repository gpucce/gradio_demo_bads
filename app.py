from bz2 import compress
import gradio as gr
from transformers import AutoModelForSequenceClassification, AutoTokenizer, AutoConfig
import pandas as pd
import json

with open("tag_map.json") as tag_map_file:
    tag_map = json.load(tag_map_file)

reverse_map = {j: i for i, j in tag_map.items()}

model_name_or_path = "gpucce/ProSolAdv_full_train"

config = AutoConfig.from_pretrained(model_name_or_path)
config.num_classes = len(tag_map)
model = AutoModelForSequenceClassification.from_pretrained(
    model_name_or_path, config=config
)
tokenizer = AutoTokenizer.from_pretrained(model_name_or_path)


def classify(csv_file):

    df = pd.read_csv(csv_file.name)

    preds = pd.DataFrame(["" for _ in range(len(df))], columns=["preds"])
    for idx, sent in enumerate(df.text):

        pred = (
            reverse_map[
                model(**tokenizer(sent, return_tensors="pt")).logits.argmax(-1).item()
            ]
            .replace("_", " ")
            .capitalize()
        )

        preds.iloc[idx, 0] = pred
    output_file_name = "gradio_demo_output.csv.zip"
    preds.to_csv(output_file_name, index=False, compression="zip")
    return output_file_name


iface = gr.Interface(fn=classify, inputs="file", outputs="file")
iface.launch()
