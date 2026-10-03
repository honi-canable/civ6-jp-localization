--====================================================================================================================
-- LocalizedText
--====================================================================================================================
INSERT OR REPLACE INTO LocalizedText
		(
			Tag,
			Language,
			Text
		)
VALUES
--====================================================================================================================
-- Screenshot Mode
--====================================================================================================================
	-- Buttons
	-----------------------------------------------------
		(
			"LOC_SUK_SCREENSHOT_MODE_NAME",
			"en_US",
			"Screenshot Mode"
		),
		(
			"LOC_SUK_SCREENSHOT_MODE_TT",
			"en_US",
			"Left-click to enter Screenshot Mode with the current settings. Right-click to open the Screenshot Mode options panel."
		),
		(
			"LOC_SUK_SCREENSHOT_MODE_DESC",
			"en_US",
			"Enter Screenshot Mode.[NEWLINE][NEWLINE] Screenshot Mode will hide most or all UI elements, allowing you to take unobstructed screenshots.[NEWLINE][NEWLINE] You may pan the screen with the WASD keys; rotate with the Q and E keys; hold Alt and use the Mouse Wheel to adjust Time of Day; and if Fixed Tilt is enabled, you can adjust the tilt with the Z and C keys. Camera rotation will not snap back while in this mode.[NEWLINE][NEWLINE] Press ESC to exit Screenshot Mode."
		),
	-----------------------------------------------------
	-- Hotkeys
	-----------------------------------------------------
		(
			"LOC_OPTIONS_HOTKEY_SUK_SCREENSHOT_MODE",
			"en_US",
			"Enter {LOC_SUK_SCREENSHOT_MODE_NAME}"
		),
		(
			"LOC_OPTIONS_HOTKEY_SUK_SCREENSHOT_MODE_HELP",
			"en_US",
			"Enters {LOC_SUK_SCREENSHOT_MODE_NAME}"
		),
	-----------------------------------------------------
	-- Options
	-----------------------------------------------------
		(
			"LOC_SUK_SCREENSHOT_MODE_FIXED_TILT_NAME",
			"en_US",
			"Use Fixed Tilt"
		),
		(
			"LOC_SUK_SCREENSHOT_MODE_FIXED_TILT_DESC",
			"en_US",
			"Use Fixed Tilt in Screenshot Mode. You may Alt + Drag to adjust tilt, or use the Z and C keys.[NEWLINE][NEWLINE][COLOR_RED]Warning: Certain angles and tilts may cause the game to crash. Be cautious![ENDCOLOR]"
		),
		(
			"LOC_SUK_SCREENSHOT_MODE_UNIT_FLAG_NAME",
			"en_US",
			"Hide Unit Flags"
		),
		(
			"LOC_SUK_SCREENSHOT_MODE_UNIT_FLAG_DESC",
			"en_US",
			"Hide Unit Flags in Screenshot Mode."
		),
		(
			"LOC_SUK_SCREENSHOT_MODE_CITY_BANNER_NAME",
			"en_US",
			"Hide City Banners"
		),
		(
			"LOC_SUK_SCREENSHOT_MODE_CITY_BANNER_DESC",
			"en_US",
			"Hide City Banners in Screenshot Mode."
		),
		(
			"LOC_SUK_SCREENSHOT_MODE_BORDERS_NAME",
			"en_US",
			"Hide Borders"
		),
		(
			"LOC_SUK_SCREENSHOT_MODE_BORDERS_DESC",
			"en_US",
			"Hide Borders in Screenshot Mode."
		),
		(
			"LOC_SUK_SCREENSHOT_MODE_MAP_LABELS_NAME",
			"en_US",
			"Hide Map Labels"
		),
		(
			"LOC_SUK_SCREENSHOT_MODE_MAP_LABELS_DESC",
			"en_US",
			"Hide Map Labels in Screenshot Mode, if they aren't already hidden."
		),
		(
			"LOC_SUK_SCREENSHOT_MODE_YIELDS_NAME",
			"en_US",
			"Hide Yields"
		),
		(
			"LOC_SUK_SCREENSHOT_MODE_YIELDS_DESC",
			"en_US",
			"Hide Yields in Screenshot Mode, if they aren't already hidden."
		),
		(
			"LOC_SUK_SCREENSHOT_MODE_RESOURCE_ICONS_NAME",
			"en_US",
			"Hide Resource Icons"
		),
		(
			"LOC_SUK_SCREENSHOT_MODE_RESOURCE_ICONS_DESC",
			"en_US",
			"Hide Resource Icons in Screenshot Mode, if they aren't already hidden."
		),
		(
			"LOC_SUK_SCREENSHOT_MODE_MAP_PINS_NAME",
			"en_US",
			"Hide Map Pins"
		),
		(
			"LOC_SUK_SCREENSHOT_MODE_MAP_PINS_DESC",
			"en_US",
			"Hide Map Pins in Screenshot Mode."
		),
--====================================================================================================================
-- Production Tooltip
--====================================================================================================================
		(
			"LOC_CITY_YIELD_FROM_BUILDINGS_SUMMARY_TOOLTIP",
			"en_US",
			"{Value : number +#.#;-#.#} from Buildings (Total)"
		),
		(
			"LOC_CITY_YIELD_FROM_DISTRICTS_SUMMARY_TOOLTIP",
			"en_US",
			"{Value : number +#.#;-#.#} from Districts (Total)"
		),

		(
			"LOC_CITY_GET_UNIT_PRODUCTION_MODIFIER",
			"en_US",
			"{Value : number +#;-#}% ({ActualValue : number +#.#;-#.#}) towards Units"
		),
		(
			"LOC_CITY_GET_BUILDING_PRODUCTION_MODIFIER",
			"en_US",
			"{Value : number +#;-#}% ({ActualValue : number +#.#;-#.#}) towards Buildings and Wonders"
		),
		(
			"LOC_CITY_GET_BUILDING_NON_WONDER_PRODUCTION_MODIFIER",
			"en_US",
			"{Value : number +#;-#}% ({ActualValue : number +#.#;-#.#}) towards Buildings"
		),
--====================================================================================================================
-- Growth and District Tooltips
--====================================================================================================================
		(
			"LOC_SUK_DISTRICT_POPULATION_TOOLTIP",
			"en_US",
			"The District cap will next increase at {2} [ICON_Citizen] Population. You can currently build up to {1} Districts."
		),
		(
			"LOC_SUK_CITY_YIELD_FROM_POPULATION_TOOLTIP",
			"en_US",
			"{1} from Population"
		),
		(
			"LOC_SUK_CITY_YIELD_FROM_HAPPINESS_TOOLTIP",
			"en_US",
			"{1}% ({2}) from Amenities"
		),
		(
			"LOC_SUK_CITY_YIELD_FROM_HOUSING_TOOLTIP",
			"en_US",
			"{1}% ({2}) from Housing"
		),
		(
			"LOC_SUK_CITY_YIELD_FROM_OCCUPATION_TOOLTIP",
			"en_US",
			"{1}% ({2}) from Occupation"
		),
--====================================================================================================================
-- Loyalty Tooltips
--====================================================================================================================
		(
			"LOC_SUK_LOYALTY_HEADER_TOOLTIP",
			"en_US",
			"Pressure from nearby Citizens"
		),
		(
			"LOC_SUK_LOYALTY_TOTAL_POPULATION_PRESSURE_TOOLTIP",
			"en_US",
			"Total Pop. Pressure"
		),
		(
			"LOC_SUK_LOYALTY_CAP_INFO_TOOLTIP",
			"en_US",
			"Population Pressure scales based on the ratio between Domestic and Foreign Pressure. Population Pressure is always capped at ±20."
		),
		(
			"LOC_SUK_LOYALTY_CAP_TOOLTIP",
			"en_US",
			"(will be capped at ±20)"
		),
--====================================================================================================================
-- Religion Tooltips
--====================================================================================================================
		(
			"LOC_SUK_RELIGION_TOOLTIP_PRESSURE_ICON",
			"en_US",
			"[ICON_Religion]"
		),
--====================================================================================================================
-- City Panel Overview
--====================================================================================================================
		(
			"LOC_HUD_REPORTS_SUK_OTHER_ADJACENCY_BONUS",
			"en_US",
			"Other Bonuses"
		),
--====================================================================================================================
-- Misc.
--====================================================================================================================
		(
			"LOC_CITY_YIELD_FROM_GREATWORKS_TOOLTIP",
			"en_US",
			"{Value : number +#.#;-#.#} from Great Works"
		),
		(
			"LOC_OPTIONS_HOTKEY_CATEGORY_SUK_HOTKEYS",
			"en_US",
			"User Interface (Sukritact’s Mods):"
		);



--====================================================================================================================
-- Japanese
--====================================================================================================================
INSERT OR REPLACE INTO LocalizedText
		(
			Tag,
			Language,
			Text
		)
VALUES
--====================================================================================================================
-- Screenshot Mode
--====================================================================================================================
	-- Buttons
	-----------------------------------------------------
		(
			"LOC_SUK_SCREENSHOT_MODE_NAME",
			"ja_JP",
			"スクリーンショットモード"
		),
		(
			"LOC_SUK_SCREENSHOT_MODE_TT",
			"ja_JP",
			"左クリック: スクリーンショットモードに切り替え[NEWLINE]右クリック: 撮影オプションの設定"
		),
		(
			"LOC_SUK_SCREENSHOT_MODE_DESC",
			"ja_JP",
			"スクリーンショットモードを実行します。ほとんどのUI要素が非表示になり、視界を妨げずにスクリーンショットを撮影できます。[NEWLINE][NEWLINE]平行移動: WASDキー[NEWLINE]回転: Q, Eキー[NEWLINE]光源調整: Alt+マウスホイール[NEWLINE]傾斜: Z, Cキー (オプションでカメラの固定を有効化時)[NEWLINE]終了: ESCキー"
		),
	-----------------------------------------------------
	-- Hotkeys
	-----------------------------------------------------
		(
			"LOC_OPTIONS_HOTKEY_SUK_SCREENSHOT_MODE",
			"ja_JP",
			"{LOC_SUK_SCREENSHOT_MODE_NAME}に移行"
		),
		(
			"LOC_OPTIONS_HOTKEY_SUK_SCREENSHOT_MODE_HELP",
			"ja_JP",
			"{LOC_SUK_SCREENSHOT_MODE_NAME}に移行"
		),
	-----------------------------------------------------
	-- Options
	-----------------------------------------------------
		(
			"LOC_SUK_SCREENSHOT_MODE_FIXED_TILT_NAME",
			"ja_JP",
			"カメラの固定"
		),
		(
			"LOC_SUK_SCREENSHOT_MODE_FIXED_TILT_DESC",
			"ja_JP",
			"スクリーンショットモード中のカメラを固定する。Alt+ドラッグまたはZ, Cキーで傾斜を調整する。[NEWLINE][NEWLINE][COLOR_RED]警告: 特定の角度や傾斜によってはゲームがクラッシュする可能性があります。注意してください。[ENDCOLOR]"
		),
		(
			"LOC_SUK_SCREENSHOT_MODE_UNIT_FLAG_NAME",
			"ja_JP",
			"ユニットフラグの非表示"
		),
		(
			"LOC_SUK_SCREENSHOT_MODE_UNIT_FLAG_DESC",
			"ja_JP",
			"撮影モード中、ユニットフラグを非表示にする。"
		),
		(
			"LOC_SUK_SCREENSHOT_MODE_CITY_BANNER_NAME",
			"ja_JP",
			"都市バナーの非表示"
		),
		(
			"LOC_SUK_SCREENSHOT_MODE_CITY_BANNER_DESC",
			"ja_JP",
			"撮影モード中、都市バナーを非表示にする。"
		),
		(
			"LOC_SUK_SCREENSHOT_MODE_BORDERS_NAME",
			"ja_JP",
			"境界線の非表示"
		),
		(
			"LOC_SUK_SCREENSHOT_MODE_BORDERS_DESC",
			"ja_JP",
			"撮影モード中、境界線を非表示にする。"
		),
		(
			"LOC_SUK_SCREENSHOT_MODE_MAP_LABELS_NAME",
			"ja_JP",
			"マップラベルの非表示"
		),
		(
			"LOC_SUK_SCREENSHOT_MODE_MAP_LABELS_DESC",
			"ja_JP",
			"撮影モード中、マップラベルを非表示にする。"
		),
		(
			"LOC_SUK_SCREENSHOT_MODE_YIELDS_NAME",
			"ja_JP",
			"産出アイコンの非表示"
		),
		(
			"LOC_SUK_SCREENSHOT_MODE_YIELDS_DESC",
			"ja_JP",
			"撮影モード中、産出アイコンを非表示にする。(マップに表示中の場合)"
		),
		(
			"LOC_SUK_SCREENSHOT_MODE_RESOURCE_ICONS_NAME",
			"ja_JP",
			"資源アイコンの非表示"
		),
		(
			"LOC_SUK_SCREENSHOT_MODE_RESOURCE_ICONS_DESC",
			"ja_JP",
			"撮影モード中、資源アイコンを非表示にする。(マップに表示中の場合)"
		),
		(
			"LOC_SUK_SCREENSHOT_MODE_MAP_PINS_NAME",
			"ja_JP",
			"マップピンの非表示"
		),
		(
			"LOC_SUK_SCREENSHOT_MODE_MAP_PINS_DESC",
			"ja_JP",
			"撮影モード中、マップピンを非表示にする。"
		),
--====================================================================================================================
-- Production Tooltip
--====================================================================================================================
		(
			"LOC_CITY_YIELD_FROM_BUILDINGS_SUMMARY_TOOLTIP",
			"ja_JP",
			"建造物により (合計) {Value : number +#.#;-#.#}"
		),
		(
			"LOC_CITY_YIELD_FROM_DISTRICTS_SUMMARY_TOOLTIP",
			"ja_JP",
			"区域により (合計) {Value : number +#.#;-#.#}"
		),

		(
			"LOC_CITY_GET_UNIT_PRODUCTION_MODIFIER",
			"ja_JP",
			"ユニットに対して{Value : number +#;-#}% ({ActualValue : number +#.#;-#.#})"
		),
		(
			"LOC_CITY_GET_BUILDING_PRODUCTION_MODIFIER",
			"ja_JP",
			"建造物、遺産に対して{Value : number +#;-#}% ({ActualValue : number +#.#;-#.#})"
		),
		(
			"LOC_CITY_GET_BUILDING_NON_WONDER_PRODUCTION_MODIFIER",
			"ja_JP",
			"建造物に対して{Value : number +#;-#}% ({ActualValue : number +#.#;-#.#})"
		),
--====================================================================================================================
-- Growth and District Tooltips
--====================================================================================================================
		(
			"LOC_SUK_DISTRICT_POPULATION_TOOLTIP",
			"ja_JP",
			"区域の上限は、[ICON_Citizen] 人口が{2}人になると増加する。現在は{1}つまで建設できる。"
		),
		(
			"LOC_SUK_CITY_YIELD_FROM_POPULATION_TOOLTIP",
			"ja_JP",
			"人口により{1}"
		),
		(
			"LOC_SUK_CITY_YIELD_FROM_HAPPINESS_TOOLTIP",
			"ja_JP",
			"快適性により{1}% ({2})"
		),
		(
			"LOC_SUK_CITY_YIELD_FROM_HOUSING_TOOLTIP",
			"ja_JP",
			"住宅により{1}% ({2})"
		),
		(
			"LOC_SUK_CITY_YIELD_FROM_OCCUPATION_TOOLTIP",
			"ja_JP",
			"専門家により{1}% ({2})"
		),
--====================================================================================================================
-- Loyalty Tooltips
--====================================================================================================================
		(
			"LOC_SUK_LOYALTY_HEADER_TOOLTIP",
			"ja_JP",
			"近隣の市民からの圧力"
		),
		(
			"LOC_SUK_LOYALTY_TOTAL_POPULATION_PRESSURE_TOOLTIP",
			"ja_JP",
			"総人口による圧力"
		),
		(
			"LOC_SUK_LOYALTY_CAP_INFO_TOOLTIP",
			"ja_JP",
			"人口による圧力は、その都市の所有者に属する近隣市民と他文明に属する近隣市民双方の圧力の比較により、+20から-20の間で増減する。"
		),
		(
			"LOC_SUK_LOYALTY_CAP_TOOLTIP",
			"ja_JP",
			"(±20に制限される)"
		),
--====================================================================================================================
-- Religion Tooltips
--====================================================================================================================
		(
			"LOC_SUK_RELIGION_TOOLTIP_PRESSURE_ICON",
			"ja_JP",
			"[ICON_Religion]"
		),
--====================================================================================================================
-- City Panel Overview
--====================================================================================================================
		(
			"LOC_HUD_REPORTS_SUK_OTHER_ADJACENCY_BONUS",
			"ja_JP",
			"その他のボーナス"
		),
--====================================================================================================================
-- Misc.
--====================================================================================================================
		(
			"LOC_CITY_YIELD_FROM_GREATWORKS_TOOLTIP",
			"ja_JP",
			"傑作により{Value : number +#.#;-#.#}"
		),
		(
			"LOC_OPTIONS_HOTKEY_CATEGORY_SUK_HOTKEYS",
			"ja_JP",
			"UI (Sukritact氏のMOD):"
		);
--====================================================================================================================
--====================================================================================================================