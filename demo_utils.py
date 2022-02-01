def extract_gaze_for_events(gaze_all, sections, column_timestamps="timestamp [ns]"):
    for section_idx in sections.index:
        event_pair = sections.loc[section_idx]

        mask_gaze_in_recording = gaze_all["recording id"] == event_pair["recording id"]
        mask_gaze_between_events = gaze_all[column_timestamps].between(
            event_pair["section start time [ns]"], event_pair["section end time [ns]"]
        )
        yield event_pair, gaze_all.loc[
            mask_gaze_in_recording & mask_gaze_between_events
        ].copy()


def assign_sub_aois(
    aoi_mapped_gaze, sub_aois, names=None, column_name="sub-aoi", default_value=None
):
    if names is None:
        names = [f"{column_name}-{idx}" for idx in range(len(sub_aois))]
    aoi_mapped_gaze[column_name] = default_value

    column_gaze_pos = "gaze position in reference image {} [px]"
    for name, aoi in zip(names, sub_aois):
        x, y, width, height = aoi

        x_check = aoi_mapped_gaze[column_gaze_pos.format("x")].between(x, x + width)
        y_check = aoi_mapped_gaze[column_gaze_pos.format("y")].between(y, y + height)
        aoi_mapped_gaze.loc[x_check & y_check, column_name] = name


def _enrichment_name_from_export_folder(folder_name):
    return folder_name.split("_REFERENCE-IMAGE-MAPPER_")[-1].replace("_csv", "")
