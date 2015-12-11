# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

from v1teamdata import *;

class v1PlanningLevel:
    def __init__(self,name,start_date,end_date):
        self._name = name;
        self._teams = list();
        self._start_date = start_date;
        self._end_date = end_date;
        
    def get_name(self): return self._name;
    
    def get_v1_format_start_date(self):
        return self._start_date.strftime("%Y-%m-%d");
    
    def get_v1_format_end_date(self):
        return self._end_date.strftime("%Y-%m-%d");
    
    def is_team_known(self,team_name):
        team = None;
        for t in self._teams:
            if(t.get_name() == team_name):
                team = t;
                break;
        return team;
    
    def add_team(self,team_name):
        if(team_name):
            team = self.is_team_known(team_name);
            if(not team):
                team = v1TeamData(team_name)
                #print "~~~~~~~~~~~~~~adding team" + team_name;
                self._teams.append(team);
            return team;
        
    def get_team(self,team_name):
        return self.is_team_known(team_name);
    
    def get_number_of_teams(self):
        return len(self._teams);
        
    def add_epic_for_team(self, team_name, epic):
        team = self.add_team(team_name);
        team.add_epic(epic.Number, epic.Name);
        
    def add_story_for_team(self, team_name, story_number, story_name, scope, time_box_name, time_box_begin_date, epic_id):
        team = self.add_team(team_name);
        team.add_story(story_number, story_name, scope, time_box_name, time_box_begin_date, epic_id);
    
    def map_teams_stories_to_epics(self):
        for team in self._teams:
            team.map_stories_to_epics();

    def show_all_teams_and_stories(self):
        for team in self._teams:
            print "Team:" + team.get_name();
            team.show_all_stories();
        return;
    
    def show_all_teams_and_epics(self):
        for team in self._teams:
            print "Team:" + team.get_name();
            team.show_all_epics();
        return;