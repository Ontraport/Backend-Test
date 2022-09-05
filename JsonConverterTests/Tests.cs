using JsonConverter;
using Newtonsoft.Json.Linq;
using System.Text.RegularExpressions;

namespace JsonConverterTests
{
    [TestClass]
    public class JsonConverterTests
    {
        [TestClass]
        public class Tests
        {
            #region Constants
            private const string SIMPLEJSONCONTIANER = @"{
                                                        'one':
                                                        {
                                                            'two': 3,
                                                            'four': [ 5,6,7]
                                                        },
                                                        'eight':
                                                        {
                                                            'nine':
                                                            {
                                                                'ten':11
                                                            }
                                                        }
                                                    }";

            private const string SIMPLEFLATTENEDCONTIANER = @"{
                                                            'one/two':3,
                                                            'one/four/0':5,
                                                            'one/four/1':6,
                                                            'one/four/2':7,
                                                            'eight/nine/ten':11
                                                          }";

            private const string COMPLEXJSONCONTIANER = @"{
                                                        'one':
                                                        {
                                                            'two': 3,
                                                            'four': [ 5,6,7],
                                                            'five': 
                                                            {
                                                                'six':
                                                                {
                                                                    'seven': [ 8,9,10 ]
                                                                },
                                                                'sixteen':
                                                                {
                                                                    'seventeen': [ 18,19,20 ],
                                                                    'eighteen': 88
                                                                },
                                                                'fifty':
                                                                {
                                                                    'sixty': 61
                                                                }
                                                            }
                                                        },
                                                        'eight':
                                                        {
                                                            'nine':
                                                            {
                                                                'ten':11
                                                            }
                                                        }
                                                    }";

            private const string COMPLEXFLATTENEDCONTIANER = @"{
                                                            'one/two':3,
                                                            'one/four/0':5,
                                                            'one/four/1':6,
                                                            'one/four/2':7,
                                                            'one/five/six/seven/0':8,
                                                            'one/five/six/seven/1':9,
                                                            'one/five/six/seven/2':10,
                                                            'one/five/sixteen/seventeen/0':18,
                                                            'one/five/sixteen/seventeen/1':19,
                                                            'one/five/sixteen/seventeen/2':20,
                                                            'one/five/sixteen/eighteen':88,
                                                            'one/five/fifty/sixty':61,
                                                            'eight/nine/ten':11
                                                            }";

            private const string COMPLEXJSONCONTIANER_WITHNULLVALUE = @"{
                                                        'one':
                                                        {
                                                            'two': 3,
                                                            'four': [ 5,6,7],
                                                            'five': 
                                                            {
                                                                'six':
                                                                {
                                                                    'seven': [ 8,9,10 ]
                                                                },
                                                                'sixteen':
                                                                {
                                                                    'seventeen': [ 18,19,20 ],
                                                                    'hundred':,
                                                                    'eighteen': 88
                                                                },
                                                                'fifty':
                                                                {
                                                                    'sixty': 61
                                                                }
                                                            }
                                                        },
                                                        'eight':
                                                        {
                                                            'nine':
                                                            {
                                                                'ten':11
                                                            }
                                                        }
                                                    }";

            private const string COMPLEXJSONCONTIANER_WITHNULLOBJECT = @"{
                                                        'one':
                                                        {
                                                            'two': 3,
                                                            'four': [ 5,6,7],
                                                            'five': 
                                                            {
                                                                'six':
                                                                {
                                                                    'seven': [ 8,9,10 ]
                                                                },
                                                                'sixteen':
                                                                {
                                                                    'seventeen': [ 18,19,20 ],
                                                                    'hundred':{},
                                                                    'eighteen': 88
                                                                },
                                                                'fifty':
                                                                {
                                                                    'sixty': 61
                                                                }
                                                            }
                                                        },
                                                        'eight':
                                                        {
                                                            'nine':
                                                            {
                                                                'ten':11
                                                            }
                                                        }
                                                    }";
            
            private const string COMPLEXJSONCONTIANER_WITHEMPTYVALUEARRAY = @"{
                                                        'one':
                                                        {
                                                            'two': 3,
                                                            'four': [ 5,6,7],
                                                            'five': 
                                                            {
                                                                'six':
                                                                {
                                                                    'seven': [ 8,9,10 ]
                                                                },
                                                                'sixteen':
                                                                {
                                                                    'seventeen': [ 18,19,20 ],
                                                                    'hundred':[],
                                                                    'eighteen': 88
                                                                },
                                                                'fifty':
                                                                {
                                                                    'sixty': 61
                                                                }
                                                            }
                                                        },
                                                        'eight':
                                                        {
                                                            'nine':
                                                            {
                                                                'ten':11
                                                            }
                                                        }
                                                    }";
            #endregion

            #region Fields
            private readonly Regex sWhitespace = new Regex(@"\s+");
            #endregion

            #region Methods

            #region Tests
            [TestMethod]
            public void TestSimpleJsonConversion()
            {
                TestJsonConversion(SIMPLEJSONCONTIANER, SIMPLEFLATTENEDCONTIANER);
            }

            [TestMethod]
            public void TestComplexJsonConversion()
            {
                TestJsonConversion(COMPLEXJSONCONTIANER, COMPLEXFLATTENEDCONTIANER);
            }

            [TestMethod]
            public void TestComplexJsonConversion_WithNullValue()
            {
                TestJsonConversion(COMPLEXJSONCONTIANER_WITHNULLVALUE, COMPLEXFLATTENEDCONTIANER);
            }

            [TestMethod]
            public void TestComplexJsonConversion_WithNullObject()
            {
                TestJsonConversion(COMPLEXJSONCONTIANER_WITHNULLOBJECT, COMPLEXFLATTENEDCONTIANER);
            }

            [TestMethod]
            public void TestComplexJsonConversion_WithNullValueArray()
            {
                TestJsonConversion(COMPLEXJSONCONTIANER_WITHEMPTYVALUEARRAY, COMPLEXFLATTENEDCONTIANER);
            }

            [TestMethod]
            public void TestSimpleFlattenedContainerConversion()
            {
                TestFlattenendContainerConversion(SIMPLEFLATTENEDCONTIANER, SIMPLEJSONCONTIANER);
            }

            [TestMethod]
            public void TestComplexFlattenedContainerConversion()
            {
                TestFlattenendContainerConversion( COMPLEXFLATTENEDCONTIANER, COMPLEXJSONCONTIANER);
            }

            private void TestJsonConversion(string jsonContainer, string convertedFlattenedContainer)
            {
                Dictionary<string, JToken> multiDimentionalContainer = Newtonsoft.Json.JsonConvert.DeserializeObject<Dictionary<string, JToken>>(jsonContainer);
                Dictionary<string, object> oneDimentionalContainer = JsonConverter.JsonConverter.OneDimentionalDictionary_Create(multiDimentionalContainer);
                string resultString = ReplaceWhitespace(JsonHelper.SerializeWithCustomIndenting(oneDimentionalContainer));
                string expectedResultString = ReplaceWhitespace(convertedFlattenedContainer);

                Assert.IsTrue(resultString.Equals(expectedResultString));
            }

            private void TestFlattenendContainerConversion(string flattenedContainer, string convertedJsonContainer)
            {
                Dictionary<string, object> oneDimentionalContainer = Newtonsoft.Json.JsonConvert.DeserializeObject<Dictionary<string, object>>(flattenedContainer);
                Dictionary<string,JToken> multiDimentionalContainer = JsonConverter.JsonConverter.MultiDimentionalJsonContainer_Create(oneDimentionalContainer);
                string resultString = ReplaceWhitespace(JsonHelper.SerializeWithCustomIndenting(multiDimentionalContainer));
                string expectedResultString = ReplaceWhitespace(convertedJsonContainer);

                Assert.IsTrue(resultString.Equals(expectedResultString));
            }
            #endregion

            #region Helper Methods
            private string ReplaceWhitespace(string input)
            {
                return sWhitespace.Replace(input, string.Empty);
            }
            #endregion

            #endregion
        }
    }
}