#include "trait_validation.hpp"

#include <cstdint>
#include <nlohmann/json.hpp>
#include <regex>
#include <string>

#include "errors.hpp"
#include "key_map.hpp"

void validate_traits(std::string adminType, nlohmann::json* traits_p,
                     nlohmann::json* errors_p) {
  // Parses the json for the traits (segment-trait information) passed in a
  // json object and validates the structure, format and types of this data
  std::string current_segment = "", item_segment, item_trait, item_operator;
  const char* translatedKey;

  std::regex segment_trait_key_regex{R"~((([a-z]*):*)([a-z]*):(.*))~"};
  std::smatch segment_trait_key_data;

  for (const auto& item : traits_p->items()) {
    if (!regex_match(item.key(), segment_trait_key_data,
                     segment_trait_key_regex)) {
      // Track any entries that do not match proper syntax
      update_error_json(errors_p, BAD_TRAIT_STRUCTURE,
                        nlohmann::json{
                            {"trait", item.key()}
      });
      continue;
    }
    if (segment_trait_key_data[3] == "") {
      item_operator = "";
      item_segment  = segment_trait_key_data[2];
    } else {
      item_operator = segment_trait_key_data[2];
      item_segment  = segment_trait_key_data[3];
    }
    item_trait = segment_trait_key_data[4];

    // Get passed operation and validate it
    int8_t init_trait_operator = map_operator(item_operator);
    int8_t trait_operator      = init_trait_operator;
    if (trait_operator == OPERATOR_BAD) {
      update_error_json(errors_p, BAD_OPERATOR,
                        nlohmann::json{
                            {"operator", item_operator}
      });
      continue;
    }
    int8_t trait_type = map_trait_type(item.value());
    if ((trait_operator == OPERATOR_DELETE) &&
        (trait_type != TRAIT_TYPE_NULL)) {
      update_error_json(errors_p, BAD_VALUE_FOR_DELETE,
                        nlohmann::json{
                            {  "trait",   item_trait},
                            {"segment", item_segment}
      });
    }
    if (trait_type == TRAIT_TYPE_NULL) {
      // Validate that NULL is not used with non-delete operator specified
      if ((trait_operator != OPERATOR_ANY) &&
          (trait_operator != OPERATOR_DELETE)) {
        update_error_json(errors_p, NULL_NOT_ALLOWED_OPERATOR,
                          nlohmann::json{
                              {"operator", item_operator},
                              {   "trait",    item_trait},
                              { "segment",  item_segment}
        });
        continue;
      }
      trait_operator = OPERATOR_DELETE;
    }
    if (trait_type == TRAIT_TYPE_BOOLEAN) {
      // Set operator based on boolean value
      trait_operator = (item.value()) ? OPERATOR_SET : OPERATOR_DELETE;
    }
    int8_t expected_type =
        get_racf_trait_type(adminType.c_str(), item_segment.c_str(),
                            (item_segment + ":" + item_trait).c_str());
    // Validate Segment-Trait by ensuring a TRAIT_TYPE is found
    if (expected_type == TRAIT_TYPE_BAD) {
      update_error_json(errors_p, BAD_SEGMENT_TRAIT_COMBO,
                        nlohmann::json{
                            {"segment", item_segment},
                            {  "trait",   item_trait}
      });
      continue;
    }
    if ((expected_type == TRAIT_TYPE_BOOLEAN) &&
        (trait_type == TRAIT_TYPE_NULL) &&
        (trait_operator != init_trait_operator)) {
      // Validate that NULL is not used for Boolean Segment-Traits
      update_error_json(errors_p, NULL_NOT_ALLOWED_OPERATOR,
                        nlohmann::json{
                            { "segment",  item_segment},
                            {   "trait",    item_trait},
                            {"operator", item_operator}
      });
      continue;
    }
    validate_json_value_to_string(item, expected_type, errors_p);
    // Ensure that the type of data provided for the trait matches the
    // expected TRAIT_TYPE
    if ((trait_type != expected_type) && !(trait_type == TRAIT_TYPE_NULL)) {
      update_error_json(
          errors_p, BAD_TRAIT_DATA_TYPE,
          nlohmann::json{
              {        "trait",    item.key()},
              {"required_type", expected_type}
      });
      continue;
    }
    translatedKey = get_racf_key(adminType.c_str(), item_segment.c_str(),
                                 (item_segment + ":" + item_trait).c_str(),
                                 trait_type, trait_operator);
    // If we could not find the RACF key with this function, the operation is
    // bad because we check the Segment-Trait combination above
    if ((translatedKey == NULL) && (trait_operator == init_trait_operator)) {
      update_error_json(errors_p, BAD_TRAIT_OPERATOR_COMBO,
                        nlohmann::json{
                            {"operator", item_operator},
                            { "segment",  item_segment},
                            {   "trait",    item_trait}
      });
    } else if ((translatedKey == NULL) && (trait_type != TRAIT_TYPE_NULL)) {
      // Validate that the boolean-influenced operator is allowed
      update_error_json(errors_p, BAD_BOOLEAN_OPERATOR_COMBO,
                        nlohmann::json{
                            {  "value", item.value()},
                            {"segment", item_segment},
                            {  "trait",   item_trait}
      });
    } else if (translatedKey == NULL) {
      // Validate that NULL is not used for Segment-Traits that don't allow
      // DELETE
      update_error_json(errors_p, NULL_NOT_ALLOWED_TRAIT,
                        nlohmann::json{
                            {"segment", item_segment},
                            {  "trait",   item_trait}
      });
    }
    // Passed all of our validation so we go around the loop again
  }
}

void validate_json_value_to_string(const nlohmann::json& trait,
                                   char expected_type,
                                   nlohmann::json* errors_p) {
  if (trait.is_string()) {
    return;
  }
  if (trait.is_array()) {
    for (const auto& item : trait.items()) {
      if (!item.value().is_string()) {
        update_error_json(
            errors_p, BAD_TRAIT_DATA_TYPE,
            nlohmann::json{
                {        "trait",    item.key()},
                {"required_type", expected_type}
        });
        return;
      }
    }
  }
}
