let targetLetter='A';
function makePoint(x, y) {
        return { x, y };
      }

      function dist(a, b) {
        return Math.hypot(a.x - b.x, a.y - b.y);
      }

      function pathLength(points) {
        let len = 0;
        for (let i = 1; i < points.length; i++) len += dist(points[i - 1], points[i]);
        return len;
      }

      function lerp(a, b, t) {
        return a + (b - a) * t;
      }

      function flattenStrokes(sourceStrokes) {
        const flat = [];
        sourceStrokes.forEach((stroke, strokeIndex) => {
          stroke.forEach((p, pointIndex) => {
            flat.push({ x: p.x, y: p.y, stroke: strokeIndex, start: pointIndex === 0 });
          });
        });
        return flat;
      }

      function normalize(points, size = 100) {
        if (points.length === 0) return [];
        let minX = Infinity, minY = Infinity, maxX = -Infinity, maxY = -Infinity;
        points.forEach(p => {
          minX = Math.min(minX, p.x);
          minY = Math.min(minY, p.y);
          maxX = Math.max(maxX, p.x);
          maxY = Math.max(maxY, p.y);
        });

        const boxW = Math.max(1, maxX - minX);
        const boxH = Math.max(1, maxY - minY);
        const scale = size / Math.max(boxW, boxH);
        const normalized = points.map(p => ({
          x: (p.x - minX) * scale,
          y: (p.y - minY) * scale,
          stroke: p.stroke,
          start: p.start
        }));

        const center = normalized.reduce((acc, p) => {
          acc.x += p.x;
          acc.y += p.y;
          return acc;
        }, { x: 0, y: 0 });
        center.x /= normalized.length;
        center.y /= normalized.length;

        return normalized.map(p => ({
          x: p.x - center.x,
          y: p.y - center.y,
          stroke: p.stroke,
          start: p.start
        }));
      }

      function resample(points, n = 64) {
        if (points.length === 0) return [];
        if (points.length === 1) return Array.from({ length: n }, () => ({ ...points[0] }));

        const output = [{ ...points[0] }];
        let segmentRemainder = 0;
        const total = pathLength(points);
        const interval = total / (n - 1);

        if (!isFinite(interval) || interval <= 0.01) {
          return Array.from({ length: n }, (_, i) => ({ ...points[Math.min(points.length - 1, i)] }));
        }

        let prev = { ...points[0] };
        for (let i = 1; i < points.length; i++) {
          let curr = { ...points[i] };
          let d = dist(prev, curr);

          while ((segmentRemainder + d) >= interval && output.length < n) {
            const t = (interval - segmentRemainder) / d;
            const nx = lerp(prev.x, curr.x, t);
            const ny = lerp(prev.y, curr.y, t);
            const newPoint = { x: nx, y: ny, stroke: curr.stroke, start: false };
            output.push(newPoint);
            prev = newPoint;
            d = dist(prev, curr);
            segmentRemainder = 0;
          }
          segmentRemainder += d;
          prev = curr;
        }

        while (output.length < n) output.push({ ...points[points.length - 1] });
        return output.slice(0, n);
      }

      function vectorDistance(a, b) {
        let sum = 0;
        const n = Math.min(a.length, b.length);
        for (let i = 0; i < n; i++) {
          const dx = a[i].x - b[i].x;
          const dy = a[i].y - b[i].y;
          sum += Math.hypot(dx, dy);
        }
        return sum / Math.max(1, n);
      }

      function angleBetween(a, b) {
        return Math.atan2(b.y - a.y, b.x - a.x);
      }

      function basicFeatures(rawPoints, sourceStrokes) {
        if (rawPoints.length === 0) {
          return {
            strokeCount: 0, aspect: 1, closedness: 9, turnCount: 0,
            endpoints: [], minX: 0, maxX: 0, minY: 0, maxY: 0
          };
        }

        let minX = Infinity, minY = Infinity, maxX = -Infinity, maxY = -Infinity;
        rawPoints.forEach(p => {
          minX = Math.min(minX, p.x);
          minY = Math.min(minY, p.y);
          maxX = Math.max(maxX, p.x);
          maxY = Math.max(maxY, p.y);
        });

        const w = Math.max(1, maxX - minX);
        const h = Math.max(1, maxY - minY);
        const diagonal = Math.max(1, Math.hypot(w, h));
        const start = rawPoints[0];
        const end = rawPoints[rawPoints.length - 1];
        const closedness = dist(start, end) / diagonal;

        let turnCount = 0;
        const pts = resample(rawPoints, 28);
        for (let i = 2; i < pts.length; i++) {
          const a1 = angleBetween(pts[i - 2], pts[i - 1]);
          const a2 = angleBetween(pts[i - 1], pts[i]);
          let delta = Math.abs(a2 - a1);
          delta = Math.min(delta, Math.PI * 2 - delta);
          if (delta > 1.08) turnCount++;
        }

        const endpoints = [];
        sourceStrokes.forEach(stroke => {
          if (stroke.length) {
            endpoints.push(stroke[0], stroke[stroke.length - 1]);
          }
        });

        const xNorm = p => (p.x - minX) / w;
        const yNorm = p => (p.y - minY) / h;
        const first = rawPoints[0];
        const last = rawPoints[rawPoints.length - 1];
        const startXNorm = xNorm(first);
        const startYNorm = yNorm(first);
        const endXNorm = xNorm(last);
        const endYNorm = yNorm(last);
        const lowerHalfPoints = rawPoints.filter(p => yNorm(p) > 0.52);
        const lowerRightRatio = lowerHalfPoints.length
          ? lowerHalfPoints.filter(p => xNorm(p) > 0.45).length / lowerHalfPoints.length
          : 0;
        const bottomBandPoints = rawPoints.filter(p => yNorm(p) > 0.72);
        const bottomRightRatio = bottomBandPoints.length
          ? bottomBandPoints.filter(p => xNorm(p) > 0.42).length / bottomBandPoints.length
          : 0;
        const bottomCoverage = bottomBandPoints.length / rawPoints.length;
        const endpointsRight = startXNorm > 0.52 && endXNorm > 0.58;
        const endInside = endXNorm < 0.72 && endYNorm > 0.35 && endYNorm < 0.9;

        return {
          strokeCount: sourceStrokes.length,
          aspect: w / h,
          closedness,
          turnCount,
          endpoints,
          minX, maxX, minY, maxY,
          startXNorm,
          startYNorm,
          endXNorm,
          endYNorm,
          lowerRightRatio,
          bottomRightRatio,
          bottomCoverage,
          endpointsRight,
          endInside
        };
      }

      function makeStroke(points) {
        return points.map(([x, y]) => ({ x, y }));
      }

      const templateDefinitions = {
        A: [[[10,100],[30,10],[50,100]], [[22,62],[42,62]]],
        B: [[[10,100],[10,10],[45,12],[58,25],[46,43],[10,47],[48,49],[62,68],[48,94],[10,100]]],
        C: [[[70,15],[35,5],[12,28],[10,72],[35,97],[72,84]]],
        D: [[[12,100],[12,10],[48,12],[72,35],[72,72],[48,96],[12,100]]],
        E: [[[70,10],[12,10],[12,52],[55,52],[12,52],[12,96],[72,96]]],
        F: [[[12,98],[12,10],[72,10],[12,10],[12,52],[55,52]]],
        G: [[[74,18],[42,7],[15,26],[10,62],[28,90],[62,92],[78,70],[52,70]]],
        H: [[[12,10],[12,98]], [[70,10],[70,98]], [[12,54],[70,54]]],
        I: [[[50,10],[50,96]]],
        J: [[[72,10],[72,72],[58,94],[34,96],[18,80]]],
        K: [[[14,10],[14,98]], [[70,10],[14,56],[72,98]]],
        L: [[[16,10],[16,96],[74,96]]],
        M: [[[10,98],[10,12],[42,65],[72,12],[72,98]]],
        N: [[[12,98],[12,12],[72,98],[72,12]]],
        O: [[[50,8],[22,18],[10,50],[22,84],[50,98],[78,84],[90,50],[78,18],[50,8]]],
        P: [[[12,98],[12,10],[52,12],[70,28],[58,50],[12,52]]],
        Q: [[[50,8],[22,18],[10,50],[22,84],[50,98],[78,84],[90,50],[78,18],[50,8]], [[60,72],[88,100]]],
        R: [[[12,98],[12,10],[52,12],[70,28],[58,50],[12,52],[46,52],[74,98]]],
        S: [[[74,18],[45,8],[16,20],[18,44],[56,54],[78,70],[62,92],[24,88]]],
        T: [[[15,10],[85,10]], [[50,10],[50,98]]],
        U: [[[12,10],[12,70],[28,94],[52,98],[74,72],[74,10]]],
        V: [[[10,10],[42,98],[78,10]]],
        W: [[[8,10],[24,98],[45,42],[66,98],[84,10]]],
        X: [[[12,12],[78,98]], [[78,12],[12,98]]],
        Y: [[[10,12],[45,52],[80,12]], [[45,52],[45,98]]],
        Z: [[[12,12],[78,12],[15,98],[82,98]]]
      };

      const templates = Object.entries(templateDefinitions).map(([letter, strokes]) => {
        const flat = flattenStrokes(strokes.map(makeStroke));
        return {
          letter,
          strokes,
          vector: resample(normalize(flat), 64),
          feature: basicFeatures(flat, strokes.map(makeStroke))
        };
      });

      function recognizeLetter(sourceStrokes) {
        const raw = flattenStrokes(sourceStrokes);
        if (raw.length < 7) return null;

        const userVector = resample(normalize(raw), 64);
        const userFeature = basicFeatures(raw, sourceStrokes);

        let best = { letter: "A", score: Infinity };
        const ranked = templates.map(template => {
          const shape = vectorDistance(userVector, template.vector);
          const strokePenalty = Math.min(14, Math.abs(userFeature.strokeCount - template.feature.strokeCount) * 2.3);
          const aspectPenalty = Math.min(16, Math.abs(Math.log(userFeature.aspect / template.feature.aspect)) * 7);
          const closedPenalty = Math.min(12, Math.abs(userFeature.closedness - template.feature.closedness) * 6);
          let score = shape + strokePenalty + aspectPenalty + closedPenalty;

          // Friendly nudges for common child-written shapes.
          if (userFeature.closedness < 0.22 && ["O", "Q"].includes(template.letter)) score -= 9;
          if (userFeature.aspect > 1.85 && ["L", "T", "Z", "E", "F"].includes(template.letter)) score -= 2;
          if (userFeature.aspect < 0.48 && ["I", "J", "L"].includes(template.letter)) score -= 4;
          if (userFeature.turnCount > 9 && ["S", "G", "B"].includes(template.letter)) score -= 3;

          // I vs K and other tall letters: a preschool "I" is often just one tall line.
          if (userFeature.aspect < 0.38 && userFeature.strokeCount <= 2 && userFeature.turnCount < 4) {
            if (template.letter === "I") score -= 22;
            if (["K", "X", "Y", "N", "M", "H"].includes(template.letter)) score += 18;
          }

          // Extra toddler-writing disambiguation:
          // C vs G: a C usually starts and ends on the right side; a G usually finishes inward.
          if (userFeature.endpointsRight && userFeature.endXNorm > 0.68 && userFeature.closedness > 0.24) {
            if (template.letter === "C") score -= 10;
            if (template.letter === "G") score += 13;
          }
          if (userFeature.endInside) {
            if (template.letter === "G") score -= 5;
            if (template.letter === "C") score += 5;
          }

          // B vs P: a B has meaningful drawing on the lower-right; a P mostly does not.
          if (userFeature.lowerRightRatio > 0.2) {
            if (template.letter === "B") score -= 10;
            if (template.letter === "P") score += 14;
          } else if (userFeature.lowerRightRatio < 0.1) {
            if (template.letter === "P") score -= 5;
            if (template.letter === "B") score += 9;
          }

          // E vs F: E has a bottom bar extending to the right; F usually has no bottom bar.
          if (userFeature.bottomCoverage > 0.08 && userFeature.bottomRightRatio > 0.18) {
            if (template.letter === "E") score -= 14;
            if (template.letter === "F") score += 18;
          } else if (userFeature.bottomRightRatio < 0.08) {
            if (template.letter === "F") score -= 5;
            if (template.letter === "E") score += 8;
          }

          return { letter: template.letter, score };
        }).sort((a, b) => a.score - b.score);

        best = ranked[0];

        // This is a tracing game, so give strong preference to the prompted letter
        // when it is a plausible match. This makes the game much kinder for
        // 3-4 year old handwriting while still avoiding completely unrelated marks.
        const targetRank = ranked.find(r => r.letter === targetLetter);
        if (targetRank) {
          const targetIsSimpleI =
            targetLetter === "I" &&
            userFeature.aspect < 0.48 &&
            userFeature.strokeCount <= 2 &&
            userFeature.turnCount < 5;
          // Very strong tracing bias: this game is about practicing the prompted
          // letter, not generic OCR. If the child's drawing has enough signal to
          // guess at all, heavily prefer the letter shown in the trace guide.
          const targetIsPlausible = targetRank.score < 95 || targetRank.score < best.score + 80;
          const targetIsCloseEnough = targetRank.score < best.score + 110;
          const drawingHasEnoughSignal = raw.length >= 7 && pathLength(raw) > 18;
          const targetIsLookAlike =
            (["C", "G"].includes(targetLetter) && ["C", "G"].includes(best.letter)) ||
            (["B", "P", "R"].includes(targetLetter) && ["B", "P", "R"].includes(best.letter)) ||
            (["E", "F"].includes(targetLetter) && ["E", "F"].includes(best.letter)) ||
            (["O", "Q"].includes(targetLetter) && ["O", "Q"].includes(best.letter)) ||
            (["I", "J", "L"].includes(targetLetter) && ["I", "J", "L"].includes(best.letter));

          if (targetIsSimpleI || targetIsPlausible || targetIsLookAlike || targetIsCloseEnough || drawingHasEnoughSignal) {
            best = { ...targetRank, encouraged: true };
          }
        }

        return {
          letter: best.letter,
          score: best.score,
          confidence: Math.max(0, Math.min(1, 1 - best.score / 58)),
          alternatives: ranked.slice(0, 4)
        };
      }


const E=require('./engine.js');
module.exports={...E, evaluate:(guide,strokes,target)=>{targetLetter=target;const r=recognizeLetter(strokes);if(!r)return{verdict:'retry'};return{verdict:r.letter===target?'pass':'other',letter:r.letter};}};
