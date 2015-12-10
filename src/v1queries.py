from v1pysdk import V1Meta
from datetime import *
from v1planninglevel import *
import re
import sys
import logging

logger = logging.getLogger('v1');

class v1Queries:
    (PLANNING_NAME, PLANNING_BEGIN_DATE, PLANNING_END_DATE) = (0, 1, 2);
    def __init__(self, url, usr, pw):
        with V1Meta(
            instance_url = url,
            username = usr,
            password = pw
        ) as v1:
            self._v1 = v1;
                
    def get_planning_levels_for(self, parent_planning_level, planning_levels):
        filterTerm="Scope.Parent.Name='" + parent_planning_level + "'";
        scopes = self._v1.Scope.select('Name','BeginDate','Parent','EndDate').filter(filterTerm);
        for scope in scopes:
            ##print scope;
            ##print scope.Name + ":" + scope.BeginDate + ":" + scope.EndDate;
            #if(scope.Parent): print ">>>>>>>>>>" + scope.Parent.Name;
            end_date = datetime.strptime(scope.EndDate, "%Y-%m-%d");
            begin_date = datetime.strptime(scope.BeginDate, "%Y-%m-%d");
            today = datetime.today()
            planning_levels.append((scope.Name, begin_date, end_date));
            if(today >= begin_date and today <= end_date \
            and scope.Name <> 'PPAPI' \
            and scope.Name <> 'SP 2015.09 (PSI) - SAT>IP core player'): # Hack to remove PPAPI and SAT>IP as it runs till 2017
                active_planning_level = (scope.Name, begin_date, end_date);
        return active_planning_level;
        
    def get_stories_for_planning_level(self, planningLevel):
        filterTerm="Scope.Name='" + planningLevel.get_name() + "'";
        stories = self._v1.Story.select('Number', 'Name', 'Scope', 'Team', 'Super', 'Timebox', 'Custom_ReviewStatus2').filter(filterTerm);
        return stories;
    
    def get_defects_for_planning_level(self, planningLevel):
        filterTerm="Scope.Name='" + planningLevel.get_name() + "'";
        defects = self._v1.Defect.select('Number', 'Name', 'Scope', 'Team', 'Super', 'Timebox').filter(filterTerm);
        return defects;
        
#    def get_support_item_type(self, item):
#        support_item = v1TeamData.NOT_SUPPORT;
#        if item.Super and re.match(r'\[\w+\s\w+\]\sSafe\s+&\s+PI\sSupport', item.Super.Name):
#            #print "Found SAFE and PI Support Epic: " + story.Super.Name;
#            support_item = v1TeamData.SAFE_PI_SUPPORT;
#        elif item.Super and re.match(r'\[\w+\s\w+\]\sCustomer\sIntegration,\sMaintenance\sand\sSupport', item.Super.Name):
#            #print "Found SAFE and PI Support Epic: " + story.Super.Name;
#            support_item = v1TeamData.CUSTOMER_SUPPORT;
#        return support_item;    
    
    def parse_stories_into_teams(self, add_story_for_team_callback, stories):
        for story in stories:
            team_name = story.Team.Name if story.Team else "UNSPECIFIED TEAM";
            time_box_name = story.Timebox.Name if story.Timebox else "not planned";
            time_box_begin_date = datetime.strptime(story.Timebox.BeginDate, "%Y-%m-%d") if story.Timebox else datetime(9999,12,31);
            epic_id = story.Super.Number if story.Super.Number else "NO EPIC";
            add_story_for_team_callback(team_name, story.Number, story.Name, story.Scope.Name, time_box_name, time_box_begin_date, epic_id)
        return;
    
#    def parse_defects_into_teams(self, planning_level, defects):
#        for defect in defects:
#            team_name = defect.Team.Name if defect.Team else "UNSPECIFIED TEAM";
#            team = planning_level.add_team(team_name);
#            tb_name = defect.Timebox.Name if defect.Timebox else "not planned";
#            tb_begin_date = datetime.strptime(defect.Timebox.BeginDate, "%Y-%m-%d") if defect.Timebox else datetime(9999,12,31);
#            # Get the number of hrs spent in support
#            #print "super number=" + story.Super.Number + " epic=" + planning_level.get_support_epic_numbers();
#            support_type = self.get_support_item_type(defect);
#            if support_type <>  v1TeamData.NOT_SUPPORT:
#                #print "Found Support story: " + story.Number;
#                actual_hrs = self.get_story_task_actuals(defect.Number, planning_level.get_v1_format_start_date(), planning_level.get_v1_format_end_date());
#                team.add_support_item(defect.Number, defect.Name, tb_name, tb_begin_date, actual_hrs, support_type)
#        return;
    
    def is_for_the_ios_team(self, epic_name):
        return (re.match( r'\[[iI]OS\s(HTML|SDK)\s*(4.0)*\]', epic_name)\
            or re.match( r'\[Handheld\s+[iI]OS\s*\]', epic_name)\
            or re.match( r'\[[iI]OS\s*\]', epic_name));
            
    def is_for_the_android_team(self, epic_name):
        return (re.match( r'\[Android\s*(HTML|SDK)\s*(Native|Nex|4.0)*', epic_name)\
                or re.match( r'\[Android\s*(Native|Nex)\s*(HTML|SDK)\s*', epic_name)\
                or re.match( r'\[Handheld\s+Android\s*\]', epic_name)\
                or re.match( r'\[Android\s*\]', epic_name));
            
    def is_for_the_desktop_team(self, epic_name):
        return (re.match( r'\[(Win|[oO]SX)\s*BP NPAPI\s*]', epic_name)\
                        or re.match( r'\[(Win|[oO]SX)\s*HTML\s*]', epic_name)\
                        or re.match( r'\[Desktop\s+NPAPI\s*\]', epic_name)
                        or re.match( r'\[NaC[lL]\s*BP\s*PPAPI\s*]', epic_name)\
                        or re.match( r'\[(Win)*\s*BP\s*NaC[lL]\s*]', epic_name)\
                        or re.match( r'\[Desktop\s+PPAPI\s*\]', epic_name)\
                        or re.match( r'\[Desktop\s*\]', epic_name)\
                        or re.match( r'\[(Win|[oO]SX)\s*BP\sHTML\sPlayer\s*]', epic_name));
                        
    def is_for_the_ppc_team(self, epic_name):
        return (re.match( r'\[PPC\s*\]', epic_name));
            
    def parse_epics_into_teams(self, add_epic_for_team_callback, epics):
        for epic in epics:
            if (self.is_for_the_ios_team(epic.Name)):
                #print "FOUND iOS MATCH:" + epic.Name;
                add_epic_for_team_callback("MS_NMP_iOS", epic);
            elif (self.is_for_the_android_team(epic.Name)):
                #print "FOUND Android MATCH:" + epic.Name;
                add_epic_for_team_callback("MS_NMP_Android", epic);
            elif (self.is_for_the_desktop_team(epic.Name)):
                #print "FOUND Desktop MATCH:" + epic.Name;
                add_epic_for_team_callback("MS_NMP_Desktop", epic);
            elif (self.is_for_the_ppc_team(epic.Name)):
                #print "FOUND PPC MATCH:" + epic.Name;
                add_epic_for_team_callback("MS_NMP_Portable_Component", epic);
            else:
                #print "NO MATCH:" + epic.Name;
                logger.warning("NO MATCH:" + epic.Name);
                add_epic_for_team_callback("UNSPECIFIED TEAM", epic);
        return;
    
    def get_epics_for_planning_level(self, planningLevel):
        filterTerm="Scope.Name='" + planningLevel.get_name() + "'";
        epics = self._v1.Epic.select('Number', 'Name', 'Scope', 'Custom_ReviewStatus3').filter(filterTerm);
        return epics;
    
#    def show_stories_info(self, stories):
#        print "**********************STORIES**************************"
#        for story in stories:
#            print story.Number + ":" + story.Name + ":" + story.Scope.Name + ":";
#            if(story.Custom_ReviewStatus2):
#                print "***********" + story.Custom_ReviewStatus2.Name;
#            if(story.Team):
#                print "***********" + story.Team.Name;
#        print "*******************************************************"
#        return;
#    
#    def show_epics_info(self, epics):
#        print "**********************EPICS***************************"
#        for epic in epics:
#            print epic.Number + ":" + epic.Name + ":" + epic.Scope.Name + ":";
#            if(epic.Custom_ReviewStatus3):
#                print "***********" + epic.Custom_ReviewStatus3.Name;
#        print "*******************************************************"
#        return;
#    
#    def convert_stories_to_list(self, stories, list_data):
#        for story in stories:
#            #print story.Number + ":" + story.Name + ":" + story.Scope.Name;
#            if(story.Custom_ReviewStatus2):
#                reviewStatus = story.Custom_ReviewStatus2.Name
#            else:
#                reviewStatus = "None";
#            list_data.append((story.Number, story.Name, story.Scope.Name, reviewStatus));
#        return
        