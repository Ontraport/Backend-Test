const expect = require("chai").expect;
const main = require("../main");

let objListType1 = {
    one: {
        two: 3,
        four: [5, 6, 7, 8, 9, 10],
    },
    eight: {
        nine: {
            ten: 11,
        },
    },
}

describe("Test main", function () {
    it("integration test", function () {
        const list = main(objListType1);

        expect(list).to.eql(objListType1)
    })
})

describe("Test main", function () {
    it("integration test with object parameter as empty", function () {
        const list = main({});

        expect(list).to.eql({});
    })
})

describe("Test main", function () {
    it("integration test with object parameter as null", function () {
        const list = main(null);

        expect(list).to.eql({});
    })
})
