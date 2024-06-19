def save_summaries(summaries, file_path):
    try:
        with open(file_path, "w") as f:
            for summary in summaries:
                f.write(summary + "\n\n")
        print("email summaries saved successfully!")
    except Exception as e:
        print("error saving summaries: ", e)