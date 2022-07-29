import React from "react"

const OddsDisplay = ({ odds, enable, resetTable, getAndShowOdds }) => (
  <div className="odds-container">
    <p>
      {odds
        ? "To calculate new odds, click Reset to clear the table."
        : "Once you have selected enough cards, click Calculate to see who has the better chance of winning the hand!"}
    </p>
    <button
      className={enable ? "selected-button" : "disable"}
      disabled={!enable}
      onClick={odds ? resetTable : getAndShowOdds}
    >
      {odds ? "Reset Table" : "Calculate Odds"}
    </button>
    <div className="results-container">
      {odds ? (
        <>
          <p>I would: {JSON.stringify(odds)}%</p>
        </>
      ) : (
        <p>Results will appear here...</p>
      )}
    </div>
  </div>
)

export default OddsDisplay
