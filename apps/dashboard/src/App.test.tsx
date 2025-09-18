import React from "react";

// Simple smoke test to ensure React components can be imported
test("components can be imported", () => {
  expect(React).toBeDefined();
});

test("dashboard app passes basic import test", () => {
  const App = require("./App").default;
  expect(App).toBeDefined();
});
