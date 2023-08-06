class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

class Colify():

    def __init__(self, user_data):
        self.user_data = user_data
        self.headers = user_data.keys()
        self.columns = user_data.values()  

    def max_rows(self):
        column_lengths = []
        for column in self.columns:
            column_lengths.append(len(column))
        return max(column_lengths)   

    def max_column_width(self):
        column_widths = []
        for column in self.columns:
            for word in column:
                column_widths.append(len(word))
        return max(column_widths)        

    def output_string(self):
        s= '{'
        s+=':>'
        s+=str(self.max_column_width())
        s+='} | '
        return s

    def print_headers(self):
        output = '| '
        for header in self.headers:
            output += self.output_string()
        print(color.UNDERLINE \
            + output.format(*[ word.upper() for word in self.headers]) \
            + color.END)     

    def build_line(self, i):
        values = []
        for column in self.columns:
            try:
                values.append(column[i])
            except IndexError:
                # empty value needed to preserve formatting
                values.append('')    
        template = '| '         
        for value in values:   
            template += self.output_string()    
        line = [template, values]   
        return line       
        
    def print_body(self):      
        for i in range(0, self.max_rows() -1 , 1):
            line = self.build_line(i)   
            print(line[0].format(*line[1]))

    def colify(self):
        self.print_headers()
        self.print_body()        
