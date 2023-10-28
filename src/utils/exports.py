import pandas as pd

from config import logger, FILE_OUT_BIB, FILE_OUT_CSV


# Function to save a DataFrame to a CSV file with 'title' and 'author' as the first columns
def df_to_csv(df, FILE_OUT_CSV):
    try:
        df[['title', 'author'] + [col for col in df.columns if col not in ['title', 'author']]].to_csv(FILE_OUT_CSV, index=False)
        logger.info(f"Saved DataFrame to {FILE_OUT_CSV}")
    except Exception as e:
        logger.error(f"Error saving DataFrame to CSV file {FILE_OUT_CSV}: {e}")

# Function to convert a DataFrame to BibTeX and save to a file
def df_to_bibtex(df, FILE_OUT_BIB):
    try:
        # Save the DataFrame as a CSV file with 'title' and 'author' as the first columns
        df_to_csv(df, FILE_OUT_BIB)

        # Write the BibTeX entries to the output file
        with open(FILE_OUT_BIB, 'a') as bibtex_file:
            for _, row in df.iterrows():
                cleaned_row = row.dropna()
                entry_type = cleaned_row.get('ENTRYTYPE')
                entry_id = cleaned_row.get('ID')
                bibtex_file.write(f"@{entry_type}{'{'}{entry_id},\n")

                for key, value in cleaned_row.items():
                    if key not in ['ENTRYTYPE', 'ID']:
                        bibtex_file.write(f"  {key} = {{{value}}},\n")

                bibtex_file.write("}\n")
    except Exception as e:
        logger.error(f"Error converting DataFrame to BibTeX and saving to {FILE_OUT_BIB}: {e}")

# Function to update the DataFrame with download status and URL
def update_dataframe(df, idx, status, url=None):
    try:
        df.at[idx, 'downloaded'] = status
        df.at[idx, 'downloaded_url'] = url
        return df
    except Exception as e:
        logger.error(f"Error updating the DataFrame: {e}")
        return df
