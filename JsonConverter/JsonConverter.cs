using System;
using Newtonsoft.Json.Linq;

namespace JsonConverter
{
    public static class JsonConverter
    {
        #region Constants
        private const string PATH_DELIMETER = "/";
        private const string VALUE_INDICATOR = ":";
        private const string VALUE_DELIMETER = ",";
        #endregion

        #region Fields
        private static Dictionary<string, object> _jsonObjectDictionary = new Dictionary<string, object>(StringComparer.OrdinalIgnoreCase);
        #endregion

        #region Methods

        #region Public

        /// <summary>
        /// Converts object dictionary into a JSON string.
        /// </summary>
        /// <param name="dictionary"></param>
        /// <returns></returns>
        public static string Dictionary_ToJSONString(Dictionary<string, object> dictionary)
        {
            return JsonHelper.SerializeWithCustomIndenting(dictionary);
        }

        /// <summary>
        /// Creates a multi-dimensional JSON container from a one dimensional container.
        /// Note: dictionary parameter is a key: string, value: object dictionary which can be created by deserializing a json string using Newtonsoft.Json.JsonConvert.DeserializeObject<Dictionary<string, object>(jsonString); 
        /// </summary>
        /// <param name="dictionary"></param>
        /// <returns></returns>
        public static Dictionary<string, JToken> MultiDimentionalJsonContainer_Create(Dictionary<string, object> objectDictionary)
        {
            objectDictionary = Dictionary_Simplify(objectDictionary);

            Dictionary<string, JObject> jsonObjectDictionary = new Dictionary<string, JObject>();
            foreach (KeyValuePair<string, object> pathValuePair in objectDictionary)
            {
                JObject jObject = JObject_CreateFromKeyValuePair(pathValuePair);
                if (jObject != null)
                {
                    if (jsonObjectDictionary.ContainsKey(jObject.First.Path))
                    {
                        (jsonObjectDictionary[jObject.First.Path] as JObject).Merge(jObject, new JsonMergeSettings
                        {
                            MergeArrayHandling = MergeArrayHandling.Union
                        });
                    }
                    else
                    {
                        jsonObjectDictionary.Add(jObject.First.Path, jObject);
                    }
                }
            }

            Dictionary<string, JToken> jsonTokenDictionary = new Dictionary<string, JToken>();
            foreach (KeyValuePair<string, JObject> valuePair in jsonObjectDictionary)
            {
                JProperty property = (JProperty)valuePair.Value.First;
                jsonTokenDictionary.Add(valuePair.Key, property.First);
            }

            return jsonTokenDictionary;
        }

        /// <summary>
        /// Converts a multi-dimensional container into a one dimensional dictionary.
        /// </summary>
        /// <param name="jsonTokenDictionary"></param>
        /// <returns></returns>
        public static Dictionary<string, object> OneDimentionalDictionary_Create(Dictionary<string, JToken> jsonTokenDictionary)
        {
            _jsonObjectDictionary.Clear();
            foreach (KeyValuePair<string, JToken> parentObject in jsonTokenDictionary)
            {
                ContainerList_Populate(parentObject.Value, parentObject.Key);
            }

            return _jsonObjectDictionary;
        }

        #endregion

        #region Private

        private static JObject JObject_CreateFromKeyValuePair(KeyValuePair<string, object> keyValuePair)
        {
            string jsonObjectString = string.Empty;
            object value = keyValuePair.Value;
            if (value != null)
            {
                if (value.GetType() == typeof(List<int>))
                {
                    string valueString = string.Join(VALUE_DELIMETER, value as List<int>);
                    jsonObjectString = keyValuePair.Key + VALUE_INDICATOR + "[" + valueString + "]";
                }
                else
                {
                    jsonObjectString = keyValuePair.Key + VALUE_INDICATOR + value.ToString();
                }

                jsonObjectString = ("{" + jsonObjectString).Replace(PATH_DELIMETER, VALUE_INDICATOR + "{");
                int depth = jsonObjectString.Count(x => x == '{');
                for (int i = 0; i < depth; i++)
                {
                    jsonObjectString = jsonObjectString + "}";
                }
            }
            return (JObject)JToken.Parse(jsonObjectString);
        }

        private static Dictionary<string, object> Dictionary_Simplify(Dictionary<string, object> dictionary)
        {
            int index = 0;
            int currentIndex = 0;
            string valueArrayPath = string.Empty;
            List<int> valuesAsString = new List<int>();
            Dictionary<string, object> dictionarySimplified = new Dictionary<string, object>();

            foreach (KeyValuePair<string, object> keyValuePair in dictionary)
            {
                string indexLocation = $"{PATH_DELIMETER}{index}";
                if (keyValuePair.Value != null)
                {
                    if (keyValuePair.Key.EndsWith(indexLocation))
                    {
                        valueArrayPath = keyValuePair.Key.Replace(indexLocation, string.Empty);
                        valuesAsString.Add(Convert.ToInt32(keyValuePair.Value));
                        index++;
                    }
                    else if (keyValuePair.Key.EndsWith($"{PATH_DELIMETER}0")) //In case another value array is started directly after the current value array.
                    {
                        dictionarySimplified.Add(valueArrayPath, new List<int>(valuesAsString));
                        valuesAsString.Clear();
                        valueArrayPath = keyValuePair.Key.Replace(indexLocation, string.Empty);
                        valuesAsString.Add(Convert.ToInt32(keyValuePair.Value));
                        index = 1;
                    }

                    if (valuesAsString.Count > 0)
                    {
                        if(!dictionary.ElementAt(currentIndex + 1).Key.EndsWith($"{PATH_DELIMETER}{index}"))
                        {
                            dictionarySimplified.Add(valueArrayPath, new List<int>(valuesAsString));
                            valueArrayPath = string.Empty;
                            valuesAsString.Clear();
                            index = 0;
                        }
                    }
                    else
                    {
                        dictionarySimplified.Add(keyValuePair.Key, Convert.ToInt32(keyValuePair.Value));
                    }
                }
                currentIndex++;
            }

            return dictionarySimplified;
        }

        private static void ContainerList_Populate(JToken container, string path, string name = "")
        {
            foreach (JToken child in container.Children())
            {
                if (child.HasValues)
                {
                    switch (child.Type)
                    {
                        case JTokenType.Property:
                            name = Container_GetName(child);
                            ContainerList_Populate(child, path, name);
                            break;
                        case JTokenType.Object:
                            JObject objectProp = (JObject)child;
                            foreach (JProperty property in objectProp.Properties())
                            {
                                name = Container_GetName(child.Parent);
                                path = ContainerPath_Append(path, name);

                                ContainerList_Populate(property, path, name);
                            }
                            break;
                        case JTokenType.Array:
                            JEnumerable<JToken> childValues = child.Children();

                            name = Container_GetName(child.Parent);
                            path = ContainerPath_Append(path, name);

                            int index = 0;
                            foreach (var value in childValues)
                            {
                                ContainerList_Add(path + $"{PATH_DELIMETER}{index}", value);
                                index++;
                            }
                            break;
                        default:
                            break;
                    }
                }
                else
                {
                    name = Container_GetName(child.Parent);
                    path = ContainerPath_Append(path, name);

                    if (child.Type != JTokenType.Object && child.Type != JTokenType.Array) // This is used to filter out null objects and empty arrays.
                    {
                        JValue parentProp = (JValue)child;
                        object value = parentProp.Value;
                        if (value != null)
                        {
                            ContainerList_Add(path, value);
                        } }
                }
            }
        }

        private static void ContainerList_Add(string path, object values)
        {
            _jsonObjectDictionary.Add(path, values);
        }

        private static string Container_GetName(JToken jToken)
        {
            JProperty parentProp = (JProperty)jToken;
            return parentProp.Name;
        }

        private static string ContainerPath_Append( string path, string extention )
        {
            if (!path.Contains(extention))
            {
                path = path + PATH_DELIMETER + extention;
            }

            return path;
        }
        #endregion

        #endregion
    }
}
