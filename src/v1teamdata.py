# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

from datetime import *;

class v1Story:
    def __init__(self, number, name, scope, sprint,begin_date, epic_id):
        self.number = number;
        self.name = name;
        self.scope = scope;
        self.sprint = sprint;
        self.begin_date = begin_date;
        self.epic_id = epic_id;
    
    def __str__(self):
        return "STORY:" + self.number + " " + self.name.encode('ASCII', 'ignore').strip() + \
                " " + self.scope + " " + self.sprint + \
                " " + self.begin_date.strftime("%Y-%m-%d") + " " + self.epic_id;

    def __repr__(self):
        return self.__str__(self);
    
class v1Epic:
    def __init__(self, number, name):
        self.number = number;
        self.name = name;
        self.last_story_date = datetime(9999,12,31);
        self.last_story_sprint = "Not Planned";
        self.stories = list();
        
    def __str__(self):
        story_string = "[";
        for story in self.stories:
            story_string = story_string + " " + str(story) + " |";
        story_string += "]";
        return "EPIC:" + self.number + " " + self.name.encode('ASCII', 'ignore').strip() + \
                " " + self.last_story_date.strftime("%Y-%m-%d") + " " + self.last_story_sprint + " " + story_string;
        
        def __repr__(self):
            return self.__str__(self);
            
class v1TeamData:
#    (SAFE_PI_SUPPORT,CUSTOMER_SUPPORT,NOT_SUPPORT) = (0,1,-1);
#    (STORY_NUMBER,STORY_NAME,STORY_SCOPE,STORY_SPRINT,STORY_BEGIN_DATE,STORY_EPIC_ID)  = (0,1,2,3,4,5);
#    (EPIC_NUMBER,EPIC_NAME,EPIC_STORY_LIST)  = (0,1,2);
#    (SUPPORT_ACTUAL_HRS, SUPPORT_TYPE) = (4,5);
    
    def __init__(self, team_name):
        self._name = team_name;
        self._stories = list();
        self._epics = list();
        self._rd_sup_items = list(); 
        
    def get_name(self): return self._name;
    
    def add_story(self,number,name,scope,sprint, begin_date, epic_id):
        self._stories.append(v1Story(number,name,scope,sprint,begin_date, epic_id));
        return
    
    def add_epic(self, number, name):
        self._epics.append(v1Epic(number, name));
        return;
    
    def get_epics(self):
        return self._epics;
     
    def get_story_key(_self, story):
        return story.begin_date;
    
    
    def sort_stories_by_date(self, epic):
        epic.stories.sort(key=self.get_story_key);
        if len(epic.stories):
            epic.last_story_date = epic.stories[-1].begin_date;
            epic.last_story_sprint = epic.stories[-1].sprint;
        print epic;
        #for story in epic.stories:
        #    print story;
    
    def get_epic_key(_self, epic):
        return epic.last_story_date;
    
    def sort_epics_by_last_story_date(self):
        self._epics.sort(key=self.get_epic_key);
        
    def map_stories_to_epics(self):
        print "========= Map storied to epics for " + self._name + " ============="
        for epic in self._epics:
            # Find the stories that match the epic
            for story in self._stories:
                if epic.number == story.epic_id:
                    epic.stories.append(story);
            # Sort the stories by time
            self.sort_stories_by_date(epic);
        self.sort_epics_by_last_story_date();
        print "==================================================================="
     
    
#    def add_support_item(self, number, name, sprint, begin_date, actual_hrs, support_type):
##        print number, 
##        print name.encode('ASCII', 'ignore').strip(), 
##        print sprint, 
##        print begin_date,
##        print actual_hrs, 
##        print support_type;
#        name.encode('ASCII', 'ignore').strip();
#        self._rd_sup_items.append((number, name, sprint, begin_date, actual_hrs, support_type));
#        return;
    
    def get_stories(self):
        return self._stories;
    
    def show_all_stories(self):
        for story in self._stories:
            print story;
                 
    def show_all_epics(self):
        for epic in self._epics:
            print epic;
            
    def show_all_support_stories(self):
        for item in self._rd_sup_items:
            for i in item:
                print i,;
            print "";
            
#    def get_ac_reviewed_percentage_for_stories(self):
#        ac_percent=0;
#        if(len(self._stories)):
#            reviewed = 0.0;
#            for story in self._stories:
#                #print story[len(story)-1];
#                if story[v1TeamData.STORY_REVIEW_STATUS] == "Complete":
#                    #print story[len(story)-1];
#                    reviewed += 1.0;
#            #print reviewed, len(self._stories);
#            ac_percent = (reviewed/len(self._stories)) * 100;
#        return round(ac_percent,2);
#    
#    def get_ac_reviewed_percentage_for_epics(self):
#        ac_percent=0;
#        if(len(self._epics)):
#            reviewed = 0.0;
#            for epic in self._epics:
#                #print story[len(story)-1];
#                if epic[v1TeamData.EPIC_REVIEW_STATUS] == "Complete":
#                    #print story[len(story)-1];
#                    reviewed += 1.0;
#            #print reviewed, len(self._stories);
#            ac_percent = (reviewed/len(self._epics)) * 100;
#        return round(ac_percent,2);
    
#    def get_total_support_by_type(self, type):
#        support_hrs = 0.0;
#        if len(self._rd_sup_items):
#            for item in self._rd_sup_items:
#                if item[v1TeamData.SUPPORT_ACTUAL_HRS] > 0.0\
#                and item[v1TeamData.SUPPORT_TYPE] == type:
#                    #print story[len(story)-1];
#                    support_hrs += item[v1TeamData.SUPPORT_ACTUAL_HRS];
#        return support_hrs;
