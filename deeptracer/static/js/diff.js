/**
 * diff.js - 代码Diff对比+选择+复制逻辑
 * 功能：
 * 1. 对比original_code和modified_code，生成Diff结果
 * 2. 处理用户选择（保留原代码/替换为新代码）
 * 3. 合并选择后的代码并复制到剪贴板
 */

// 改进的 Diff 算法实现，支持直接替换显示
function generateDiff(original, modified) {
    const originalLines = original.split('\n');
    const modifiedLines = modified.split('\n');
    const result = [];
    
    let i = 0, j = 0;
    let displayLineNumber = 1;
    
    while (i < originalLines.length || j < modifiedLines.length) {
        if (i < originalLines.length && j < modifiedLines.length) {
            if (originalLines[i] === modifiedLines[j]) {
                // 无变化
                result.push({
                    type: 'unchanged',
                    content: originalLines[i],
                    lineNumber: displayLineNumber++,
                    originalLineNum: i + 1,
                    modifiedLineNum: j + 1
                });
                i++;
                j++;
            } else {
                // 检查是否是修改（同一位置的内容不同）
                result.push({
                    type: 'modified',
                    originalContent: originalLines[i],
                    modifiedContent: modifiedLines[j],
                    lineNumber: displayLineNumber++,
                    originalLineNum: i + 1,
                    modifiedLineNum: j + 1
                });
                i++;
                j++;
            }
        } else if (i < originalLines.length) {
            // 剩余的原始行被删除
            result.push({
                type: 'deleted',
                content: originalLines[i],
                lineNumber: displayLineNumber++,
                originalLineNum: i + 1
            });
            i++;
        } else {
            // 剩余的修改行是新增
            result.push({
                type: 'added',
                content: modifiedLines[j],
                lineNumber: displayLineNumber++,
                modifiedLineNum: j + 1
            });
            j++;
        }
    }
    
    return result;
}

// 合并选择后的代码
function mergeCode(diffResult, selections) {
    const mergedLines = [];
    
    for (let i = 0; i < diffResult.length; i++) {
        const line = diffResult[i];
        const selection = selections[i];
        
        if (line.type === 'unchanged') {
            mergedLines.push(line.content);
        } else if (line.type === 'added') {
            // 新增行：apply=替换（添加），skip=不替换（不添加）
            if (selection === 'apply') {
                mergedLines.push(line.content);
            }
        } else if (line.type === 'deleted') {
            // 删除行：keep=保留（不删除），delete=删除（不保留）
            if (selection === 'keep') {
                mergedLines.push(line.content);
            }
        } else if (line.type === 'modified') {
            // 修改行：keep_modified=保留新代码，keep_original=保留原代码
            if (selection === 'keep_modified') {
                mergedLines.push(line.modifiedContent);
            } else {
                mergedLines.push(line.originalContent);
            }
        }
    }
    
    return mergedLines.join('\n');
}

// 复制到剪贴板
function copyToClipboard(text) {
    return new Promise((resolve, reject) => {
        if (navigator.clipboard && window.isSecureContext) {
            navigator.clipboard.writeText(text)
                .then(() => resolve())
                .catch(err => reject(err));
        } else {
            //  fallback for insecure contexts
            const textArea = document.createElement('textarea');
            textArea.value = text;
            textArea.style.position = 'fixed';
            textArea.style.left = '-999999px';
            textArea.style.top = '-999999px';
            document.body.appendChild(textArea);
            textArea.focus();
            textArea.select();
            
            try {
                document.execCommand('copy');
                resolve();
            } catch (err) {
                reject(err);
            } finally {
                document.body.removeChild(textArea);
            }
        }
    });
}