using System;
using Newtonsoft.Json;

namespace JsonConverter
{
    public static class JsonHelper
    {
        /// <summary>
        /// Creates a JSON string from an object container without indenting array values.
        /// </summary>
        /// <param name="jsonObject"></param>
        /// <returns></returns>
        public static string SerializeWithCustomIndenting(object jsonObject)
        {
            using (StringWriter sw = new StringWriter())
            {
                using (JsonWriter jw = new CustomJsonTextWriter(sw))
                {
                    JsonSerializer ser = new JsonSerializer();
                    ser.Serialize(jw, jsonObject);
                    return sw.ToString();
                }
            }
        }
    }

    #region CustomJsonTextWriterClass

    public class CustomJsonTextWriter : JsonTextWriter
    {
        #region Constructor

        /// <summary>
        /// Creates an instance of the CustomJsonTextWriter class.
        /// </summary>
        /// <param name="writer"></param>
        public CustomJsonTextWriter(TextWriter writer) : base(writer)
        {
            Formatting = Formatting.Indented;
            QuoteChar = '\'';
        }

        #endregion

        #region Methods
        protected override void WriteIndent()
        {
            if (WriteState != WriteState.Array)
            {
                base.WriteIndent();
            }
            else
            {
                WriteIndentSpace();
            }
        }
        #endregion

    }

    #endregion
}
