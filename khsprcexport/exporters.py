import json
import pypdftk


def write_json_file(output_file_name=None, data_dict=None):
    if output_file_name and data_dict:
        try:
            with open(output_file_name, 'w') as jf:
                jf.write(json.dumps(data_dict, indent=2))
            return True
        except:
            return False
    return False


def write_pdf_file(output_file_name=None, data_dict=None, pdf_template_file=None):
    if output_file_name and data_dict and pdf_template_file:
        try:
            fill_data = {}
            fill_data['Name'] = data_dict['header']['name']
            fill_data['Date immersed'] = data_dict['header']['date_immersed']
            fill_data['Date of birth'] = data_dict['header']['date_of_birth']
            if data_dict['header']['male']:
                fill_data['Check Box1'] = 'Yes'
            if data_dict['header']['female']:
                fill_data['Check Box2'] = 'Yes'
            if data_dict['header']['other_sheep']:
                fill_data['Check Box3'] = 'Yes'
            if data_dict['header']['anointed']:
                fill_data['Check Box4'] = 'Yes'
            if data_dict['header']['elder']:
                fill_data['Check Box5'] = 'Yes'
            if data_dict['header']['ministerial_servant']:
                fill_data['Check Box6'] = 'Yes'
            if data_dict['header']['regular_pioneer']:
                fill_data['Check Box7'] = 'Yes'
            service_years = list(data_dict['summary'].keys())
            if len(service_years) > 0:
                fill_data['Service Year'] = service_years[0]
                fill_data['1-Place_Total'] = data_dict['summary'][service_years[0]
                                                                  ]['total_placements']
                fill_data['1-Video_Total'] = data_dict['summary'][service_years[0]
                                                                  ]['total_video_showings']
                fill_data['1-Hours_Total'] = data_dict['summary'][service_years[0]
                                                                  ]['total_hours']
                fill_data['1-RV_Total'] = data_dict['summary'][service_years[0]
                                                               ]['total_return_visits']
                fill_data['1-Studies_Total'] = data_dict['summary'][service_years[0]
                                                                    ]['total_studies']
                fill_data['RemarksTotal'] = "%d Reports" % data_dict['summary'][service_years[0]
                                                                                ]['number_of_reports']
                fill_data['1-Place_Average'] = data_dict['summary'][service_years[0]
                                                                    ]['avg_placements']
                fill_data['1-Video_Average'] = data_dict['summary'][service_years[0]
                                                                    ]['avg_video_showings']
                fill_data['1-Hours_Average'] = data_dict['summary'][service_years[0]]['avg_hours']
                fill_data['1-RV_Average'] = data_dict['summary'][service_years[0]
                                                                 ]['avg_return_visits']
                fill_data['1-Studies_Average'] = data_dict['summary'][service_years[0]]['avg_studies']
                for rep in data_dict['reports']:
                    if rep['service_year'] == service_years[0]:
                        if rep['month'] == 9:
                            fill_data['1-Place_1'] = rep['placements']
                            fill_data['1-Video_1'] = rep['return_visits']
                            fill_data['1-Hours_1'] = rep['hours']
                            fill_data['1-RV_1'] = rep['return_visits']
                            fill_data['1-Studies_1'] = rep['studies']
                            fill_data['RemarksSeptember'] = rep['remarks']
                        if rep['month'] == 10:
                            fill_data['1-Place_2'] = rep['placements']
                            fill_data['1-Video_2'] = rep['return_visits']
                            fill_data['1-Hours_2'] = rep['hours']
                            fill_data['1-RV_2'] = rep['return_visits']
                            fill_data['1-Studies_2'] = rep['studies']
                            fill_data['RemarksOctober'] = rep['remarks']
                        if rep['month'] == 11:
                            fill_data['1-Place_3'] = rep['placements']
                            fill_data['1-Video_3'] = rep['return_visits']
                            fill_data['1-Hours_3'] = rep['hours']
                            fill_data['1-RV_3'] = rep['return_visits']
                            fill_data['1-Studies_3'] = rep['studies']
                            fill_data['RemarksNovember'] = rep['remarks']
                        if rep['month'] == 12:
                            fill_data['1-Place_4'] = rep['placements']
                            fill_data['1-Video_4'] = rep['return_visits']
                            fill_data['1-Hours_4'] = rep['hours']
                            fill_data['1-RV_4'] = rep['return_visits']
                            fill_data['1-Studies_4'] = rep['studies']
                            fill_data['RemarksDecember'] = rep['remarks']
                        if rep['month'] == 1:
                            fill_data['1-Place_5'] = rep['placements']
                            fill_data['1-Video_5'] = rep['return_visits']
                            fill_data['1-Hours_5'] = rep['hours']
                            fill_data['1-RV_5'] = rep['return_visits']
                            fill_data['1-Studies_5'] = rep['studies']
                            fill_data['RemarksJanuary'] = rep['remarks']
                        if rep['month'] == 2:
                            fill_data['1-Place_6'] = rep['placements']
                            fill_data['1-Video_6'] = rep['return_visits']
                            fill_data['1-Hours_6'] = rep['hours']
                            fill_data['1-RV_6'] = rep['return_visits']
                            fill_data['1-Studies_6'] = rep['studies']
                            fill_data['RemarksFebruary'] = rep['remarks']
                        if rep['month'] == 3:
                            fill_data['1-Place_7'] = rep['placements']
                            fill_data['1-Video_7'] = rep['return_visits']
                            fill_data['1-Hours_7'] = rep['hours']
                            fill_data['1-RV_7'] = rep['return_visits']
                            fill_data['1-Studies_7'] = rep['studies']
                            fill_data['RemarksMarch'] = rep['remarks']
                        if rep['month'] == 4:
                            fill_data['1-Place_8'] = rep['placements']
                            fill_data['1-Video_8'] = rep['return_visits']
                            fill_data['1-Hours_8'] = rep['hours']
                            fill_data['1-RV_8'] = rep['return_visits']
                            fill_data['1-Studies_8'] = rep['studies']
                            fill_data['RemarksApril'] = rep['remarks']
                        if rep['month'] == 5:
                            fill_data['1-Place_9'] = rep['placements']
                            fill_data['1-Video_9'] = rep['return_visits']
                            fill_data['1-Hours_9'] = rep['hours']
                            fill_data['1-RV_9'] = rep['return_visits']
                            fill_data['1-Studies_9'] = rep['studies']
                            fill_data['RemarksMay'] = rep['remarks']
                        if rep['month'] == 6:
                            fill_data['1-Place_10'] = rep['placements']
                            fill_data['1-Video_10'] = rep['return_visits']
                            fill_data['1-Hours_10'] = rep['hours']
                            fill_data['1-RV_10'] = rep['return_visits']
                            fill_data['1-Studies_10'] = rep['studies']
                            fill_data['RemarksJune'] = rep['remarks']
                        if rep['month'] == 7:
                            fill_data['1-Place_11'] = rep['placements']
                            fill_data['1-Video_11'] = rep['return_visits']
                            fill_data['1-Hours_11'] = rep['hours']
                            fill_data['1-RV_11'] = rep['return_visits']
                            fill_data['1-Studies_11'] = rep['studies']
                            fill_data['RemarksJuly'] = rep['remarks']
                        if rep['month'] == 8:
                            fill_data['1-Place_12'] = rep['placements']
                            fill_data['1-Video_12'] = rep['return_visits']
                            fill_data['1-Hours_12'] = rep['hours']
                            fill_data['1-RV_12'] = rep['return_visits']
                            fill_data['1-Studies_12'] = rep['studies']
                            fill_data['RemarksAugust'] = rep['remarks']
            if len(service_years) > 1:
                fill_data['Service Year_2'] = service_years[1]
                fill_data['2-Place_Total'] = data_dict['summary'][service_years[1]
                                                                  ]['total_placements']
                fill_data['2-Video_Total'] = data_dict['summary'][service_years[1]
                                                                  ]['total_video_showings']
                fill_data['2-Hours_Total'] = data_dict['summary'][service_years[1]
                                                                  ]['total_hours']
                fill_data['2-RV_Total'] = data_dict['summary'][service_years[1]
                                                               ]['total_return_visits']
                fill_data['2-Studies_Total'] = data_dict['summary'][service_years[1]
                                                                    ]['total_studies']
                fill_data['RemarksTotal_2'] = "%d Reports" % data_dict['summary'][service_years[1]
                                                                                  ]['number_of_reports']
                fill_data['2-Place_Average'] = data_dict['summary'][service_years[1]
                                                                    ]['avg_placements']
                fill_data['2-Video_Average'] = data_dict['summary'][service_years[1]
                                                                    ]['avg_video_showings']
                fill_data['2-Hours_Average'] = data_dict['summary'][service_years[1]]['avg_hours']
                fill_data['2-RV_Average'] = data_dict['summary'][service_years[1]
                                                                 ]['avg_return_visits']
                fill_data['2-Studies_Average'] = data_dict['summary'][service_years[1]]['avg_studies']
                for rep in data_dict['reports']:
                    if rep['service_year'] == service_years[1]:
                        if rep['month'] == 9:
                            fill_data['2-Place_1'] = rep['placements']
                            fill_data['2-Video_1'] = rep['return_visits']
                            fill_data['2-Hours_1'] = rep['hours']
                            fill_data['2-RV_1'] = rep['return_visits']
                            fill_data['2-Studies_1'] = rep['studies']
                            fill_data['RemarksSeptember_2'] = rep['remarks']
                        if rep['month'] == 10:
                            fill_data['2-Place_2'] = rep['placements']
                            fill_data['2-Video_2'] = rep['return_visits']
                            fill_data['2-Hours_2'] = rep['hours']
                            fill_data['2-RV_2'] = rep['return_visits']
                            fill_data['2-Studies_2'] = rep['studies']
                            fill_data['RemarksOctober_2'] = rep['remarks']
                        if rep['month'] == 11:
                            fill_data['2-Place_3'] = rep['placements']
                            fill_data['2-Video_3'] = rep['return_visits']
                            fill_data['2-Hours_3'] = rep['hours']
                            fill_data['2-RV_3'] = rep['return_visits']
                            fill_data['2-Studies_3'] = rep['studies']
                            fill_data['RemarksNovember_2'] = rep['remarks']
                        if rep['month'] == 12:
                            fill_data['2-Place_4'] = rep['placements']
                            fill_data['2-Video_4'] = rep['return_visits']
                            fill_data['2-Hours_4'] = rep['hours']
                            fill_data['2-RV_4'] = rep['return_visits']
                            fill_data['2-Studies_4'] = rep['studies']
                            fill_data['RemarksDecember_2'] = rep['remarks']
                        if rep['month'] == 1:
                            fill_data['2-Place_5'] = rep['placements']
                            fill_data['2-Video_5'] = rep['return_visits']
                            fill_data['2-Hours_5'] = rep['hours']
                            fill_data['2-RV_5'] = rep['return_visits']
                            fill_data['2-Studies_5'] = rep['studies']
                            fill_data['RemarksJanuary_2'] = rep['remarks']
                        if rep['month'] == 2:
                            fill_data['2-Place_6'] = rep['placements']
                            fill_data['2-Video_6'] = rep['return_visits']
                            fill_data['2-Hours_6'] = rep['hours']
                            fill_data['2-RV_6'] = rep['return_visits']
                            fill_data['2-Studies_6'] = rep['studies']
                            fill_data['RemarksFebruary_2'] = rep['remarks']
                        if rep['month'] == 3:
                            fill_data['2-Place_7'] = rep['placements']
                            fill_data['2-Video_7'] = rep['return_visits']
                            fill_data['2-Hours_7'] = rep['hours']
                            fill_data['2-RV_7'] = rep['return_visits']
                            fill_data['2-Studies_7'] = rep['studies']
                            fill_data['RemarksMarch_2'] = rep['remarks']
                        if rep['month'] == 4:
                            fill_data['2-Place_8'] = rep['placements']
                            fill_data['2-Video_8'] = rep['return_visits']
                            fill_data['2-Hours_8'] = rep['hours']
                            fill_data['2-RV_8'] = rep['return_visits']
                            fill_data['2-Studies_8'] = rep['studies']
                            fill_data['RemarksApril_2'] = rep['remarks']
                        if rep['month'] == 5:
                            fill_data['2-Place_9'] = rep['placements']
                            fill_data['2-Video_9'] = rep['return_visits']
                            fill_data['2-Hours_9'] = rep['hours']
                            fill_data['2-RV_9'] = rep['return_visits']
                            fill_data['2-Studies_9'] = rep['studies']
                            fill_data['RemarksMay_2'] = rep['remarks']
                        if rep['month'] == 6:
                            fill_data['2-Place_10'] = rep['placements']
                            fill_data['2-Video_10'] = rep['return_visits']
                            fill_data['2-Hours_10'] = rep['hours']
                            fill_data['2-RV_10'] = rep['return_visits']
                            fill_data['2-Studies_10'] = rep['studies']
                            fill_data['RemarksJune_2'] = rep['remarks']
                        if rep['month'] == 7:
                            fill_data['2-Place_11'] = rep['placements']
                            fill_data['2-Video_11'] = rep['return_visits']
                            fill_data['2-Hours_11'] = rep['hours']
                            fill_data['2-RV_11'] = rep['return_visits']
                            fill_data['2-Studies_11'] = rep['studies']
                            fill_data['RemarksJuly_2'] = rep['remarks']
                        if rep['month'] == 8:
                            fill_data['2-Place_12'] = rep['placements']
                            fill_data['2-Video_12'] = rep['return_visits']
                            fill_data['2-Hours_12'] = rep['hours']
                            fill_data['2-RV_12'] = rep['return_visits']
                            fill_data['2-Studies_12'] = rep['studies']
                            fill_data['RemarksAugust_2'] = rep['remarks']
            pypdftk.fill_form(pdf_template_file, fill_data, output_file_name)
            return True
        except:
            return False
    return False
