using JsonConverter;
using Newtonsoft.Json.Linq;

namespace JsonConverterForm
{
    public partial class JsonConverterForm : Form
    {
        public JsonConverterForm()
        {
            InitializeComponent();
        }

        private void rbToOneDimensionlContainer_CheckedChanged(object sender, EventArgs e)
        {
            if (rbToOneDimensionlContainer.Checked)
            {
                rbToMultiDimensionlContainer.Checked = false;
            }
            else
            {
                rbToMultiDimensionlContainer.Checked = true;
            }
        }

        private void rbToMultiDimensionlContainer_CheckedChanged(object sender, EventArgs e)
        {
            tbOutput.Text = string.Empty;
            tbInput.Text = string.Empty;

            if (rbToMultiDimensionlContainer.Checked)
            {
                rbToOneDimensionlContainer.Checked = false;
            }
            else
            {
                rbToOneDimensionlContainer.Checked = true;
            }
        }

        private void btnConvert_Click(object sender, EventArgs e)
        {
            Dictionary<string, JToken> multiDimentionalContainer = new Dictionary<string, JToken>();
            Dictionary<string, object> oneDimentionalContainer = new Dictionary<string, object>();

            if (tbInput.Text.Trim().Count() > 0)
            {
                if (rbToOneDimensionlContainer.Checked)
                {
                    bool jsonValid = true;

                    try
                    {
                        multiDimentionalContainer = Newtonsoft.Json.JsonConvert.DeserializeObject<Dictionary<string, JToken>>(tbInput.Text);
                    }
                    catch (Exception ex)
                    {
                        MessageBox.Show($"Error deserializing JSON string with error: {ex.Message}", "Error Deserializing JSON", MessageBoxButtons.OK, MessageBoxIcon.Error);
                        jsonValid = false;
                    }

                    if (jsonValid)
                    {
                        oneDimentionalContainer = JsonConverter.JsonConverter.OneDimentionalDictionary_Create(multiDimentionalContainer);
                        tbOutput.Text = JsonHelper.SerializeWithCustomIndenting(oneDimentionalContainer);
                    }
                }
                else
                {

                    bool jsonValid = true;
                    try
                    {
                        oneDimentionalContainer = Newtonsoft.Json.JsonConvert.DeserializeObject<Dictionary<string, object>>(tbInput.Text);
                    }
                    catch (Exception ex)
                    {
                        MessageBox.Show($"Error deserializing JSON string with error: {ex.Message}", "Error Deserializing JSON", MessageBoxButtons.OK, MessageBoxIcon.Error);
                        jsonValid = false;
                    }

                    if (jsonValid)
                    {
                        multiDimentionalContainer = JsonConverter.JsonConverter.MultiDimentionalJsonContainer_Create(oneDimentionalContainer);
                        tbOutput.Text = JsonHelper.SerializeWithCustomIndenting(multiDimentionalContainer);
                    }
                }
            }
        }
    }
}
