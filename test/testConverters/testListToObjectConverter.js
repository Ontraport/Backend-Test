const expect = require("chai").expect;
const listToObjectConverter = require('../../converters/listToObjectConverter');

let objListType1 = {
    'one/two': 3,
    'one/four/0': 5,
    'one/four/1': 6,
    'one/four/2': 7,
    'eight/nine/ten': 11
}

describe("Test listToObjectConverter", function () {
    it("converts list to object of objListType1", function () {
        const newJsonObj = listToObjectConverter(objListType1);

        expect(newJsonObj).to.eql({
                one: {
                    two: 3,
                    four: [5, 6, 7]
                }, eight: {
                    nine: {
                        ten: 11
                    }
                }
            }
        );
    });
});

let objListType2 = {
    'one/two': 3,
    'one/four/five/six/seven/0': 8,
    'eight': 11
}

describe("Test listToObjectConverter", function () {
    it("converts list to object of objListType2", function () {
        const newJsonObj = listToObjectConverter(objListType2);

        expect(newJsonObj).to.eql({
                one: {
                    two: 3,
                    four: {
                        five: {
                            six: {
                                seven: [8]
                            }
                        }
                    }
                },
                eight: 11
            }
        );
    });
});

describe("Test listToObjectConverter", function () {
    it("converts list to object with empty list", function () {
        const newJsonObj = listToObjectConverter({});

        expect(newJsonObj).to.eql({});
    });
});

describe("Test listToObjectConverter", function () {
    it("converts list to object with list parameter as null", function () {
        const newJsonObj = listToObjectConverter(null);

        expect(newJsonObj).to.eql({});
    });
});
