namespace JsonConverterForm
{
    partial class JsonConverterForm
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            System.ComponentModel.ComponentResourceManager resources = new System.ComponentModel.ComponentResourceManager(typeof(JsonConverterForm));
            this.rbToOneDimensionlContainer = new System.Windows.Forms.RadioButton();
            this.rbToMultiDimensionlContainer = new System.Windows.Forms.RadioButton();
            this.splitContainer1 = new System.Windows.Forms.SplitContainer();
            this.tbInput = new System.Windows.Forms.RichTextBox();
            this.lblInputTextBox = new System.Windows.Forms.Label();
            this.tbOutput = new System.Windows.Forms.RichTextBox();
            this.lblOutputTextBox = new System.Windows.Forms.Label();
            this.btnConvert = new System.Windows.Forms.Button();
            ((System.ComponentModel.ISupportInitialize)(this.splitContainer1)).BeginInit();
            this.splitContainer1.Panel1.SuspendLayout();
            this.splitContainer1.Panel2.SuspendLayout();
            this.splitContainer1.SuspendLayout();
            this.SuspendLayout();
            // 
            // rbToOneDimensionlContainer
            // 
            this.rbToOneDimensionlContainer.AutoSize = true;
            this.rbToOneDimensionlContainer.Checked = true;
            this.rbToOneDimensionlContainer.Location = new System.Drawing.Point(22, 9);
            this.rbToOneDimensionlContainer.Name = "rbToOneDimensionlContainer";
            this.rbToOneDimensionlContainer.Size = new System.Drawing.Size(227, 19);
            this.rbToOneDimensionlContainer.TabIndex = 0;
            this.rbToOneDimensionlContainer.TabStop = true;
            this.rbToOneDimensionlContainer.Text = "Convert to one-dimensional container";
            this.rbToOneDimensionlContainer.UseVisualStyleBackColor = true;
            this.rbToOneDimensionlContainer.CheckedChanged += new System.EventHandler(this.rbToOneDimensionlContainer_CheckedChanged);
            // 
            // rbToMultiDimensionlContainer
            // 
            this.rbToMultiDimensionlContainer.AutoSize = true;
            this.rbToMultiDimensionlContainer.Location = new System.Drawing.Point(22, 34);
            this.rbToMultiDimensionlContainer.Name = "rbToMultiDimensionlContainer";
            this.rbToMultiDimensionlContainer.Size = new System.Drawing.Size(235, 19);
            this.rbToMultiDimensionlContainer.TabIndex = 1;
            this.rbToMultiDimensionlContainer.Text = "Convert to multi-dimensional container";
            this.rbToMultiDimensionlContainer.UseVisualStyleBackColor = true;
            this.rbToMultiDimensionlContainer.CheckedChanged += new System.EventHandler(this.rbToMultiDimensionlContainer_CheckedChanged);
            // 
            // splitContainer1
            // 
            this.splitContainer1.Anchor = ((System.Windows.Forms.AnchorStyles)((((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Bottom) 
            | System.Windows.Forms.AnchorStyles.Left) 
            | System.Windows.Forms.AnchorStyles.Right)));
            this.splitContainer1.Location = new System.Drawing.Point(12, 59);
            this.splitContainer1.Name = "splitContainer1";
            // 
            // splitContainer1.Panel1
            // 
            this.splitContainer1.Panel1.Controls.Add(this.tbInput);
            this.splitContainer1.Panel1.Controls.Add(this.lblInputTextBox);
            // 
            // splitContainer1.Panel2
            // 
            this.splitContainer1.Panel2.Controls.Add(this.tbOutput);
            this.splitContainer1.Panel2.Controls.Add(this.lblOutputTextBox);
            this.splitContainer1.Size = new System.Drawing.Size(960, 362);
            this.splitContainer1.SplitterDistance = 472;
            this.splitContainer1.TabIndex = 2;
            // 
            // tbInput
            // 
            this.tbInput.Anchor = ((System.Windows.Forms.AnchorStyles)((((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Bottom) 
            | System.Windows.Forms.AnchorStyles.Left) 
            | System.Windows.Forms.AnchorStyles.Right)));
            this.tbInput.Location = new System.Drawing.Point(3, 18);
            this.tbInput.Name = "tbInput";
            this.tbInput.Size = new System.Drawing.Size(466, 341);
            this.tbInput.TabIndex = 0;
            this.tbInput.Text = "";
            // 
            // lblInputTextBox
            // 
            this.lblInputTextBox.AutoSize = true;
            this.lblInputTextBox.Location = new System.Drawing.Point(3, 0);
            this.lblInputTextBox.Name = "lblInputTextBox";
            this.lblInputTextBox.Size = new System.Drawing.Size(38, 15);
            this.lblInputTextBox.TabIndex = 3;
            this.lblInputTextBox.Text = "Input:";
            // 
            // tbOutput
            // 
            this.tbOutput.Anchor = ((System.Windows.Forms.AnchorStyles)((((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Bottom) 
            | System.Windows.Forms.AnchorStyles.Left) 
            | System.Windows.Forms.AnchorStyles.Right)));
            this.tbOutput.Location = new System.Drawing.Point(3, 18);
            this.tbOutput.Name = "tbOutput";
            this.tbOutput.Size = new System.Drawing.Size(481, 341);
            this.tbOutput.TabIndex = 0;
            this.tbOutput.Text = "";
            // 
            // lblOutputTextBox
            // 
            this.lblOutputTextBox.Anchor = ((System.Windows.Forms.AnchorStyles)(((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Left) 
            | System.Windows.Forms.AnchorStyles.Right)));
            this.lblOutputTextBox.AutoSize = true;
            this.lblOutputTextBox.Location = new System.Drawing.Point(3, 0);
            this.lblOutputTextBox.Name = "lblOutputTextBox";
            this.lblOutputTextBox.Size = new System.Drawing.Size(48, 15);
            this.lblOutputTextBox.TabIndex = 4;
            this.lblOutputTextBox.Text = "Output:";
            // 
            // btnConvert
            // 
            this.btnConvert.Anchor = ((System.Windows.Forms.AnchorStyles)((System.Windows.Forms.AnchorStyles.Bottom | System.Windows.Forms.AnchorStyles.Right)));
            this.btnConvert.Location = new System.Drawing.Point(868, 427);
            this.btnConvert.Name = "btnConvert";
            this.btnConvert.Size = new System.Drawing.Size(104, 23);
            this.btnConvert.TabIndex = 5;
            this.btnConvert.Text = "Convert";
            this.btnConvert.UseVisualStyleBackColor = true;
            this.btnConvert.Click += new System.EventHandler(this.btnConvert_Click);
            // 
            // JsonConverterForm
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(7F, 15F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(984, 461);
            this.Controls.Add(this.btnConvert);
            this.Controls.Add(this.splitContainer1);
            this.Controls.Add(this.rbToMultiDimensionlContainer);
            this.Controls.Add(this.rbToOneDimensionlContainer);
            this.Icon = ((System.Drawing.Icon)(resources.GetObject("$this.Icon")));
            this.MaximumSize = new System.Drawing.Size(1500, 700);
            this.MinimumSize = new System.Drawing.Size(700, 300);
            this.Name = "JsonConverterForm";
            this.Text = "Json Converter";
            this.splitContainer1.Panel1.ResumeLayout(false);
            this.splitContainer1.Panel1.PerformLayout();
            this.splitContainer1.Panel2.ResumeLayout(false);
            this.splitContainer1.Panel2.PerformLayout();
            ((System.ComponentModel.ISupportInitialize)(this.splitContainer1)).EndInit();
            this.splitContainer1.ResumeLayout(false);
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private RadioButton rbToOneDimensionlContainer;
        private RadioButton rbToMultiDimensionlContainer;
        private SplitContainer splitContainer1;
        private RichTextBox tbInput;
        private RichTextBox tbOutput;
        private Label lblInputTextBox;
        private Label lblOutputTextBox;
        private Button btnConvert;
    }
}