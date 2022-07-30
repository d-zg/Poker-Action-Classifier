import React from "react"

const OddsDisplay = ({ odds, enable, resetTable, calculateAction }) => (
  <div className="odds-container">
    <p>
      {odds
        ? "To calculate new action, click Reset to clear the table."
        : "Once you have selected at least your hole cards, click Calculate to see what I would do! Takes a little (~20s)"}
    </p>
    <button
      className={enable ? "selected-button" : "disable"}
      disabled={!enable}
      onClick={odds ? resetTable : calculateAction}
    >
      {odds ? "Reset Table" : "Calculate Odds"}
    </button>
    <div className="results-container">
      {odds ? (
        <>
          <p>I would: {JSON.stringify(odds)}</p>
        </>
      ) : (
        <p>Results will appear here...</p>
      )}
    </div>
  </div>
)

export default OddsDisplay
