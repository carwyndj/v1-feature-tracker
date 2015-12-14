#!/usr/bin/python2.7
# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

from v1queries import *;
from v1excelwriter import*;
import argparse;

__author__ = "jones"
__date__ = "$24-Nov-2015 14:13:55$"
__version__ = "0.1.0"

#if __name__ == "__main__
def main():
    parser = argparse.ArgumentParser(description='App to track features in an export Excel file for the current PI');
    parser.add_argument('user', help="V1 user name");
    parser.add_argument('password', help="V1 password");
    parser.add_argument('-filename', help="Excel file name to create (default is \'v1_features.xlsx\')", default="v1_features.xlsx");
    parser.add_argument('-art', help="The V1 base planning level e.g. Secure Player (ART) (default is \'Secure Player (ART)\')", default="Secure Player (ART)");
    parser.add_argument('teams', metavar='team', nargs='+', help="The V1 team to track the features for.");
    args = parser.parse_args();
  
    print "--------------------------------------"
    print "Version 1 Feature Tracking Application"
    print "--------------------------------------"

    v1q = v1Queries("https://safe.hq.k.grp/Safe", args.user, args.password);
    planning_levels = list();
    
    active_planning_level = v1q.get_planning_levels_for(args.art, planning_levels);
    
    print "The active planning level is:" + active_planning_level[v1Queries.PLANNING_NAME];
    print "***************************************************************************";
    
    v1_planning_level_obj = v1PlanningLevel(active_planning_level[v1Queries.PLANNING_NAME],
                                            active_planning_level[v1Queries.PLANNING_BEGIN_DATE],
                                            active_planning_level[v1Queries.PLANNING_END_DATE]);
    
    #Get all the epics and parse them into teams
    epics = v1q.get_epics_for_planning_level(v1_planning_level_obj);
    #v1q.show_epics_info(epics);
    v1q.parse_epics_into_teams(v1_planning_level_obj.add_epic_for_team, epics);
    #v1_planning_level_obj.show_all_teams_and_epics();
    
    #print "***************************************************************************";
    
    #Get all the stories and parse them into teams
    stories = v1q.get_stories_for_planning_level(v1_planning_level_obj);
    v1q.parse_stories_into_teams(v1_planning_level_obj.add_story_for_team, stories);
    #v1_planning_level_obj.show_all_teams_and_stories();
    
    #print "***************************************************************************";
    v1_planning_level_obj.map_teams_stories_to_epics();
    #v1_planning_level_obj.show_all_teams_and_epics();
    
    print "**************************Got V1 Information*******************************";
    print "*************************Construct Excel File******************************";
    v1_excel_writer_obj = v1ExcelWriter(args.filename);
    
    for team in args.teams:
        team_data = v1_planning_level_obj.get_team(team);
        if team_data:
            v1_excel_writer_obj.create_worksheet_for_team(team_data);
            v1_excel_writer_obj.add_headings_for_team(team_data);
            v1_excel_writer_obj.add_epics_for_team(team_data);
        else:
            print team + " Not Found"
    
    v1_excel_writer_obj.close_workbook();
    print "**********************************Done*************************************";