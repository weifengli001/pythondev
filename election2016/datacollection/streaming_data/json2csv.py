import os, csv, json
from utils.helper import make_tag
from utils.helper import text_filter
if __name__ == '__main__':

    for filename in os.listdir(os.getcwd()):
        if not filename.endswith('.json'):
            continue
        out_filename = filename[:-5]
        out_file = csv.writer(open(out_filename + ".csv", "w+"))
        with open(filename) as f:
            for line in f:
                json_data = json.loads(line)
                #out_file.writerow(["pk", "model", "codename", "name", "content_type"])
                text = text_filter(json_data['text'])
                f, tag = make_tag(text)
                if f:
                    out_file.writerow([
                            json_data['id'],
                            tag,
                            text,
                            json_data['created_at'],
                            json_data['user']['location'],
                            json_data['user']['time_zone']
                        ])

