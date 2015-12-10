# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

from v1teamdata import *;
import xlsxwriter;

class v1ExcelWorkSheetContext:
    def __init__(self, worksheet):
        self.worksheet = worksheet;
        self.next_row = 0;
        self.last_sprint_name = "None";
        self.max_column_widths = {};
        
class v1ExcelWriter:
    
    headings_dict = {"Release Number":0, "Epic Id":1, "Epic Name":2, "Story Id":3, "Story Name":4, "Story DOD Sprint":5, "Epic DOD Sprint":6 };
    
    def __init__(self, workbook_name):
        # Create an new Excel file and add a worksheet.
        self._workbook = xlsxwriter.Workbook(workbook_name)
        self._worksheet_contexts = {};
        
    def create_worksheet_for_team(self, team_data):
        worksheet = self._workbook.add_worksheet(team_data.get_name());
        self._worksheet_contexts[team_data.get_name()] = v1ExcelWorkSheetContext(worksheet);

    def get_worksheet_row_and_format(self, team_name, format_dictionary):
        worksheet = self._worksheet_contexts[team_name].worksheet;
        next_row = self._worksheet_contexts[team_name].next_row;
        format = self._workbook.add_format(format_dictionary);
        return (worksheet,next_row, format);
        
    def update_last_sprint_name_and_row(self, team_name, next_row, last_sprint_name):
        self._worksheet_contexts[team_name].next_row = next_row;
        self._worksheet_contexts[team_name].last_sprint_name = last_sprint_name;
    
    def get_last_sprint_name(self,team_name):
        return self._worksheet_contexts[team_name].last_sprint_name;
    
    def record_max_column_widths(self, team_name, current_max_widths):
        last_max_widths = self._worksheet_contexts[team_name].max_column_widths;
        
        for column_number, max_widths in current_max_widths.iteritems():
            if(last_max_widths.has_key(column_number)):
                if(last_max_widths[column_number] < max_widths):
                    last_max_widths[column_number] = max_widths;
            else:
                last_max_widths[column_number] = max_widths;
            #print team_name + " %i column width is: %i" % (column_number , last_max_widths[column_number]);
                
    def add_headings_for_team(self, team_data):
       
        (worksheet, next_row, format) = self.get_worksheet_row_and_format(
                                                        team_data.get_name(),
                                                        {'bold': True, 'font_color': 'white', 'bg_color': '#600060'})
        
        headings = v1ExcelWriter.headings_dict;
        worksheet.write(next_row, headings["Release Number"] , "Release Number", format);
        worksheet.write(next_row, headings["Epic Id"] , "Epic Id", format);
        worksheet.write(next_row, headings["Epic Name"] , "Epic Name", format);
        worksheet.write(next_row, headings["Story Id"], "Story Id", format);
        worksheet.write(next_row, headings["Story Name"], "Story Name", format);
        worksheet.write(next_row, headings["Story DOD Sprint"], "Story DOD Sprint", format);
        worksheet.write(next_row, headings["Epic DOD Sprint"], "Epic DOD Sprint", format);

        self.record_max_column_widths( team_data.get_name(),
            { headings["Release Number"] : len("Release Number"),
              headings["Epic Id"] : len("Epic Id"),
              headings["Epic Name"] : len("Epic Name"),
              headings["Story Id"] : len("Story Id"),
              headings["Story Name"] : len("Story Name"),
              headings["Story DOD Sprint"] : len("Story DOD Sprint"),
              headings["Epic DOD Sprint"] : len("Epic DOD Sprint"),
              })
              
        self._worksheet_contexts[team_data.get_name()].next_row += 1;
        
    
    def write_epic(self, team_name, epic):
        (worksheet, next_row, format) = self.get_worksheet_row_and_format(
                                                        team_name,
                                                        {'bold': True, 'bg_color': '#DDDDDD', 'left': 1, 'right': 1});
    
        if (self.get_last_sprint_name(team_name) <> epic.last_story_sprint and \
            self.get_last_sprint_name(team_name) <> "None"):
            format.set_top(6);
            
        headings = v1ExcelWriter.headings_dict;

        worksheet.write(next_row, headings["Epic Id"] , epic.number, format);
        worksheet.write(next_row, headings["Epic Name"], epic.name, format);
        worksheet.write(next_row, headings["Epic DOD Sprint"], epic.last_story_sprint, format);
        
        worksheet.write(next_row, headings["Release Number"] ,'', format);
        worksheet.write(next_row, headings["Story Id"],'', format);
        worksheet.write(next_row, headings["Story Name"],'', format);
        worksheet.write(next_row, headings["Story DOD Sprint"],'', format);
        next_row += 1;
        
        self.update_last_sprint_name_and_row(team_name, next_row, epic.last_story_sprint);

        self.record_max_column_widths(team_name,
            { headings["Epic Id"] : len(epic.number),
              headings["Epic Name"] : len(epic.name),
              headings["Epic DOD Sprint"] : len(epic.last_story_sprint)
              });
        
    def write_story(self, team_name, story):
        (worksheet, next_row, format) = self.get_worksheet_row_and_format(
                                                        team_name,
                                                        {'bg_color': '#EEEEEE', 'left': 1, 'right': 1});
        
        headings = v1ExcelWriter.headings_dict;
        
        worksheet.write(next_row, headings["Story Id"] , story.number, format);
        worksheet.write(next_row, headings["Story Name"], story.name, format);
        worksheet.write(next_row, headings["Story DOD Sprint"], story.sprint, format);
        
        worksheet.write(next_row, headings["Release Number"] ,'', format);
        worksheet.write(next_row, headings["Epic Id"] , '', format);
        worksheet.write(next_row, headings["Epic Name"], '', format);
        worksheet.write(next_row, headings["Epic DOD Sprint"], '', format);
        
        next_row += 1;
        
        self.update_last_sprint_name_and_row(team_name, next_row, story.sprint);
        
        self.record_max_column_widths(team_name,
            { headings["Story Id"] : len(story.number),
              headings["Story Name"] : len(story.name),
              headings["Story DOD Sprint"] : len(story.sprint)
              });
    
    def set_column_widths(self, team_name):
        worksheet = self._worksheet_contexts[team_name].worksheet;   
        max_column_widths = self._worksheet_contexts[team_name].max_column_widths
        for column_number, max_widths in max_column_widths.iteritems():
            worksheet.set_column(column_number, column_number, max_widths)
            
    def add_epics_for_team(self, team_data):
        for epic in team_data.get_epics():
            self.write_epic(team_data.get_name(), epic);
            for story in epic.stories:
                self.write_story(team_data.get_name(), story)
          
        self.set_column_widths(team_data.get_name());
        
                
    def close_workbook(self):
        self._workbook.close();
    
    def __del___(self):
        self.close_workbook();
        
# Widen the first column to make the text clearer.
#worksheet.set_column('A:A', 20)

# Add a bold format to use to highlight cells.
#bold = workbook.add_format({'bold': True})

# Write some simple text.
#worksheet.write('A1', 'Hello')

# Text with formatting.
#worksheet.write('A2', 'World', bold)

# Write some numbers, with row/column notation.
#worksheet.write(2, 0, 123)
#worksheet.write(3, 0, 123.456)

# Insert an image.
#worksheet.insert_image('B5', 'logo.png')

#workbook.close()

