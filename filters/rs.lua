-- The Rising-Sea papers: Pandoc filter (LaTeX output).
--   ::: {.thesis #thesis-1 title="…"}                → \begin{thesis}[…]\label{thesis-1} … \end{thesis}
--   ::: {.problem #problem-1 title="…" tags="…"}     → \RSproblem{problem-1}{…}{…}{…} … (a card)
--   ::: claim                                         → the one-sentence statement, framed (RSclaimbox)
--   ::: {.field label="Statement"}                   → a run-in small-caps card field (\RSfield); the fields
--                                                       "Statement" and "Solved when" carry a bar (RSbar)
--   ::: {.figure #fig:works file="fig-works" place="tbp"} caption :::  → a figure across the measure
--   ::: {.references}                                 → one list item per paragraph (RSreferences)
--   # Part I. The Machine {.part #part-1}             → \RSpart (paper II)
--   # Heading {.unnumbered}                           → \section*{…} once (amsart writes the contents line itself:
--                                                       pandoc's \addcontentsline made every bookmark appear twice)
-- Reports counts on stderr for tools/build.py: theses, problems, fields, figures, references.
local n = {thesis = 0, problem = 0, field = 0, figure = 0, ref = 0}
local BAR = {["Statement"] = true, ["Solved when"] = true}

local function raw(s) return pandoc.RawBlock("latex", s) end
local function latex(inlines)
  return pandoc.write(pandoc.Pandoc({pandoc.Plain(inlines)}), "latex"):gsub("%s+$", "")
end
local function inline_md(s)            -- an attribute value written in Markdown (titles: *…*, $…$) → LaTeX
  local doc = pandoc.read(s, "markdown+tex_math_dollars")
  if #doc.blocks == 0 then return "" end
  return latex(doc.blocks[1].content)
end
local function plain(s)                -- the same value for a PDF bookmark: no markup, no mathematics delimiters
  return (s:gsub("[%*%$\\{}]", ""):gsub("%^", ""):gsub("_", ""))
end

local function env(name, div)
  local opt = div.attributes.title and ("[" .. div.attributes.title .. "]") or ""
  local label = div.identifier ~= "" and ("\\label{" .. div.identifier .. "}") or ""
  local out = {raw("\\begin{" .. name .. "}" .. opt .. label)}
  for _, b in ipairs(div.content) do table.insert(out, b) end
  table.insert(out, raw("\\end{" .. name .. "}"))
  return out
end

function Header(h)
  if h.classes:includes("part") then
    local label = h.identifier ~= "" and h.identifier or ("part-" .. tostring(h.level))
    local s = pandoc.utils.stringify(h.content)
    local head, name = s:match("^(Part [IVX]+)%.%s*(.+)$")
    return raw("\\RSpart{" .. label .. "}{" .. (head or "") .. "}{" .. latex(pandoc.read(name or s, "markdown").blocks[1].content) .. "}")
  elseif h.classes:includes("unnumbered") then
    local cmd = ({"section", "subsection", "subsubsection"})[h.level] or "paragraph"
    local label = h.identifier ~= "" and ("\\label{" .. h.identifier .. "}") or ""
    local after = h.level == 2 and "\\def\\RSbmlevel{3}" or ""     -- the cards under a work of Part II
    return raw("\\" .. cmd .. "*{" .. latex(h.content) .. "}" .. label .. after)
  end
end

function Div(div)
  if div.classes:includes("thesis") then
    n.thesis = n.thesis + 1
    local out = env("thesis", div)
    out[1] = raw(out[1].text .. "\\leavevmode")   -- the heading on a line of its own, above the framed claim
    return out
  elseif div.classes:includes("problem") then
    n.problem = n.problem + 1
    local t = div.attributes.title or ""
    local out = {raw("\\RSproblem{" .. div.identifier .. "}{" .. inline_md(t) .. "}{" ..
                     (div.attributes.tags or "") .. "}{" .. plain(t) .. "}")}
    for _, b in ipairs(div.content) do table.insert(out, b) end
    table.insert(out, raw("\\par"))
    return out
  elseif div.classes:includes("claim") then
    local out = {raw("\\begin{RSclaimbox}")}
    for _, b in ipairs(div.content) do table.insert(out, b) end
    table.insert(out, raw("\\end{RSclaimbox}"))
    return out
  elseif div.classes:includes("field") then
    n.field = n.field + 1
    -- the label runs into the first paragraph of the field (a separate block would start a new paragraph)
    local lab = div.attributes.label or "?"
    local label = pandoc.RawInline("latex", "\\RSfield{" .. lab .. "}")
    local out = {}
    for i, b in ipairs(div.content) do
      if i == 1 and (b.t == "Para" or b.t == "Plain") then
        local inl = {label}
        for _, x in ipairs(b.content) do table.insert(inl, x) end
        table.insert(out, pandoc.Para(inl))
      else
        if i == 1 then table.insert(out, pandoc.Para({label})) end
        table.insert(out, b)
      end
    end
    if BAR[lab] then
      table.insert(out, 1, raw("\\begin{RSbar}"))
      table.insert(out, raw("\\end{RSbar}"))
    end
    return out
  elseif div.classes:includes("figure") then
    n.figure = n.figure + 1
    local cap = {}
    for _, b in ipairs(div.content) do
      if b.t == "Para" or b.t == "Plain" then
        if #cap > 0 then table.insert(cap, pandoc.Space()) end
        for _, x in ipairs(b.content) do table.insert(cap, x) end
      end
    end
    local place = div.attributes.place or "tbp"
    if place == "here" then           -- not floated (before a long table, which would carry a float past it)
      return raw("\\par\\begin{center}\\input{" .. div.attributes.file .. ".tex}\n\\captionof{figure}{" .. latex(cap) ..
                 "}\\label{" .. div.identifier .. "}\n\\end{center}")
    end
    -- figures/<file>.tex (tools/figures.py): the figure at its natural size, 132 mm, with its links
    return raw("\\begin{figure}[" .. place .. "]\n\\centering\\input{" .. div.attributes.file .. ".tex}\n" ..
               "\\caption{" .. latex(cap) .. "}\\label{" .. div.identifier .. "}\n\\end{figure}")
  elseif div.classes:includes("small") then          -- a table set in \small (the overview's Table 1)
    local out = {raw("\\begingroup\\small\\setlength{\\tabcolsep}{4pt}")}
    for _, b in ipairs(div.content) do table.insert(out, b) end
    table.insert(out, raw("\\endgroup"))
    return out
  elseif div.classes:includes("references") then
    local out = {raw("\\begin{RSreferences}")}
    for _, b in ipairs(div.content) do
      if b.t == "Para" then
        n.ref = n.ref + 1
        table.insert(out, raw("\\item"))
        table.insert(out, pandoc.Plain(b.content))
      end
    end
    table.insert(out, raw("\\end{RSreferences}"))
    return out
  end
end

function Pandoc(doc)
  io.stderr:write(string.format("[rs.lua] theses=%d problems=%d fields=%d figures=%d references=%d\n",
    n.thesis, n.problem, n.field, n.figure, n.ref))
  return doc
end
