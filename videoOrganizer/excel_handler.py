import pandas as pd
from api_handler import APIHandler

class ExcelHandler:
    def __init__(self, file_path):
        self.file_path = file_path
        self.df = pd.read_excel(file_path)
        self.apiHandler = APIHandler()
        self.first_column_size = 8
        self.chunk_size = 1
        self.endingPosition = 1000

    def find_empty_filename_rows(self):
        empty_filename_rows = self.df[self.df['文件名'].isna()]
        
        return empty_filename_rows.iloc[0:10]

    def get_empty_rows_in_chunks(self, chunk_size=2):
        empty_rows = self.find_empty_filename_rows()
        for i in range(0, len(empty_rows), chunk_size):
            yield empty_rows.iloc[i:i + chunk_size]

    def get_column_names(self):
        return self.df.columns.tolist()
    
    def update_excel_file(self):
        self.df.to_excel(self.file_path, index=False)

    def prepare_to_run(self):
        self.column_names = self.get_column_names()[: self.first_column_size]
        self.finalEndingPosition = min(self.endingPosition, len(self.df))

    def run(self):
        # fastForward
        counter = 0
        for i, row in self.df.iterrows():
            if i == self.endingPosition:
                break
            if not pd.isna(row['文件名']):
                counter += 1
                continue

            

        for i in range(counter, min(len(self.df), self.finalEndingPosition), self.chunk_size):
            rows = self.df.iloc[i:i + self.chunk_size]
            user_input = rows['文件路径'].tolist()
            output = self.apiHandler.call_api(user_input)
            if output is None or len(output) == 0:
                continue
            
            outputs = output.split("\n")
            outputs = [output for output in outputs if len(output.replace('`', '').replace('\n', '').strip()) > 0]

            if len(outputs) != len(rows):
                # continue
                raise Exception(f"Number of results does not match number of rows in chunk. for {outputs} for {user_input} . Returned: {len(outputs)} Expected: {len(rows)}")  
            
            for j in range(len(rows)):
                cleaned_output = outputs[j].replace('`', '').replace('\n', '').strip()
                if len(cleaned_output) == 0:
                    continue
                column_values = outputs[j].split(";")

                if len(column_values) != self.first_column_size:
                    print("Number of columns does not match number of values. for {user_input} . Returned: {column_values} Expected: {self.first_column_size}")
                    continue
                    # raise Exception("Number of columns does not match number of values. for {user_input} . Returned: {column_values} Expected: {self.first_column_size}")
                
                for k in range(self.first_column_size):
                    self.df.at[i + j, self.column_names[k]] = column_values[k]

            # Show progress bar
            progress = (i - counter) / (self.finalEndingPosition - counter) * 100
            print(f"{i}: Progress: {progress:.2f}%", end='\r')

            

# Example usage
if __name__ == "__main__":
    apiHandler = APIHandler();
    file_path = "C:\\Users\\herbe\\Downloads\\video_organize.xlsx"
    handler = ExcelHandler(file_path)
    
    handler.prepare_to_run()
    handler.run()

    # try:
    #     handler.run()
    # except Exception as e:
    #     print(f"An error occurred: {e}")
    #     handler.update_excel_file()
    #     print("Excel file updated with errors.")

    handler.update_excel_file()
    print("Excel file updated successfully.")
